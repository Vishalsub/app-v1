import sys
import json
import webbrowser
import subprocess
import time
import threading
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Signal, QTimer
import requests


class BackendChecker(QObject):
    """Backend status checker and launcher"""
    
    # Signals to communicate with QML
    statusChanged = Signal(str)  # Status message
    robotsDetected = Signal(int)  # Number of robots
    camerasDetected = Signal(int)  # Number of cameras
    backendReady = Signal(bool)  # Backend ready state
    launchReady = Signal(bool)  # Ready to launch dashboard
    
    # Properties for QML
    status = "Initializing..."
    robotCount = 0
    cameraCount = 0
    launchReady = False
    
    def __init__(self):
        super().__init__()
        self.backend_url = "http://localhost:8080"
        self.frontend_url = "http://localhost:3000"
        self.robots_count = 0
        self.cameras_count = 0
        self.backend_running = False
        self.frontend_running = False
        
        # Start checking in background
        self.start_backend_check()
    
    def start_backend_check(self):
        """Start the backend checking process"""
        self.status = "🔍 Checking backend status..."
        self.statusChanged.emit(self.status)
        
        # Check if backend is already running
        if self.check_backend_status():
            self.status = "✅ Backend already running!"
            self.statusChanged.emit(self.status)
            self.backend_running = True
            self.check_devices()
        else:
            self.status = "🚀 Starting phosphobot backend..."
            self.statusChanged.emit(self.status)
            self.start_backend()
    
    def check_backend_status(self):
        """Check if phosphobot backend is running"""
        try:
            response = requests.get(f"{self.backend_url}/status", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def start_backend(self):
        """Start the phosphobot backend in background"""
        def run_backend():
            try:
                # Start phosphobot backend
                process = subprocess.Popen([
                    "phosphobot", "run", 
                    "--port=8080", 
                    "--host=127.0.0.1", 
                    "--no-telemetry"
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Wait for backend to start
                max_wait = 30  # 30 seconds max wait
                for i in range(max_wait):
                    time.sleep(1)
                    self.status = f"⏳ Starting backend... ({i+1}/{max_wait})"
                    self.statusChanged.emit(self.status)
                    
                    if self.check_backend_status():
                        self.status = "✅ Backend started successfully!"
                        self.statusChanged.emit(self.status)
                        self.backend_running = True
                        self.check_devices()
                        return
                
                self.status = "❌ Backend startup timeout"
                self.statusChanged.emit(self.status)
                
            except Exception as e:
                self.status = f"❌ Backend startup failed: {str(e)}"
                self.statusChanged.emit(self.status)
        
        # Run in background thread
        thread = threading.Thread(target=run_backend, daemon=True)
        thread.start()
    
    def check_devices(self):
        """Check for robots and cameras"""
        self.status = "🔍 Detecting robots and cameras..."
        self.statusChanged.emit(self.status)
        
        def check_devices_thread():
            try:
                # Get status from backend
                response = requests.get(f"{self.backend_url}/status", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Count robots
                    robots = data.get('robots', [])
                    self.robots_count = len(robots)
                    
                    # Count cameras
                    cameras = data.get('cameras', [])
                    self.cameras_count = len(cameras)
                    
                    # Update UI
                    self.robotCount = self.robots_count
                    self.cameraCount = self.cameras_count
                    self.robotsDetected.emit(self.robots_count)
                    self.camerasDetected.emit(self.cameras_count)
                    
                    if self.robots_count > 0 and self.cameras_count > 0:
                        self.status = f"✅ Found {self.robots_count} robots and {self.cameras_count} cameras!"
                    elif self.robots_count > 0:
                        self.status = f"✅ Found {self.robots_count} robots!"
                    elif self.cameras_count > 0:
                        self.status = f"✅ Found {self.cameras_count} cameras!"
                    else:
                        self.status = "⚠️ No robots or cameras detected"
                    self.statusChanged.emit(self.status)
                    
                    # Start frontend
                    self.start_frontend()
                else:
                    self.status = "❌ Failed to get device status"
                    self.statusChanged.emit(self.status)
                    
            except Exception as e:
                self.status = f"❌ Device detection failed: {str(e)}"
                self.statusChanged.emit(self.status)
                # Still try to start frontend
                self.start_frontend()
        
        thread = threading.Thread(target=check_devices_thread, daemon=True)
        thread.start()
    
    def start_frontend(self):
        """Start the CEVA frontend proxy"""
        self.status = "🌐 Starting CEVA Dashboard..."
        self.statusChanged.emit(self.status)
        
        def run_frontend():
            try:
                # Start CEVA proxy server
                process = subprocess.Popen([
                    "python3", "ceva_proxy_server.py"
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Wait for frontend to start
                max_wait = 10
                for i in range(max_wait):
                    time.sleep(1)
                    try:
                        response = requests.get(self.frontend_url, timeout=2)
                        if response.status_code == 200:
                            self.frontend_running = True
                            self.status = "✅ CEVA Dashboard ready!"
                            self.statusChanged.emit(self.status)
                            self.launchReady = True
                            self.launchReady.emit(True)
                            return
                    except:
                        pass
                
                self.status = "❌ Frontend startup timeout"
                self.statusChanged.emit(self.status)
                
            except Exception as e:
                self.status = f"❌ Frontend startup failed: {str(e)}"
                self.statusChanged.emit(self.status)
        
        thread = threading.Thread(target=run_frontend, daemon=True)
        thread.start()
    
    def launch_dashboard(self):
        """Launch the CEVA Dashboard in web browser"""
        try:
            webbrowser.open(self.frontend_url)
            self.status = "🚀 Opening CEVA Dashboard..."
            self.statusChanged.emit(self.status)
        except Exception as e:
            self.status = f"❌ Failed to open browser: {str(e)}"
            self.statusChanged.emit(self.status)
    
    def get_robot_count(self):
        """Get current robot count"""
        return self.robots_count
    
    def get_camera_count(self):
        """Get current camera count"""
        return self.cameras_count
    
    def is_backend_ready(self):
        """Check if backend is ready"""
        return self.backend_running
    
    def is_launch_ready(self):
        """Check if ready to launch"""
        return self.frontend_running


def main():
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Create backend checker
    backend_checker = BackendChecker()
    
    # Register with QML
    engine.rootContext().setContextProperty("backendChecker", backend_checker)
    
    # Load QML UI
    engine.load(QUrl("main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    print("🚀 CEVA Launcher Ready.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
