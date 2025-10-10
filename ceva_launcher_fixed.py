import sys
import json
import webbrowser
import subprocess
import time
import threading
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Signal, Property, Slot
import requests


class BackendChecker(QObject):
    """Backend status checker and launcher"""
    
    # Signals to communicate with QML
    statusChanged = Signal(str)
    launchReadyChanged = Signal(bool)
    
    def __init__(self):
        super().__init__()
        self._status = "Initializing..."
        self._launch_ready = False
        
        self.backend_url = "http://localhost:8080"
        self.frontend_url = "http://localhost:3000"
        self.backend_running = False
        self.frontend_running = False
        
        # Start checking in background
        self.start_backend_check()
    
    @Property(str, notify=statusChanged)
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if self._status != value:
            self._status = value
            self.statusChanged.emit(value)


    @Property(bool, notify=launchReadyChanged)
    def launchReady(self):
        return self._launch_ready

    @launchReady.setter
    def launchReady(self, value):
        if self._launch_ready != value:
            self._launch_ready = value
            self.launchReadyChanged.emit(value)
    
    def start_backend_check(self):
        """Start the backend checking process"""
        self.status = "🔍 Checking backend status..."
        
        # Check if backend is already running
        if self.check_backend_status():
            self.status = "✅ Backend already running!"
            self.backend_running = True
            self.check_devices()
        else:
            self.status = "🚀 Starting phosphobot backend..."
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
                    
                    if self.check_backend_status():
                        self.status = "✅ Backend started successfully!"
                        self.backend_running = True
                        self.check_devices()
                        return
                
                self.status = "❌ Backend startup timeout"
                
            except Exception as e:
                self.status = f"❌ Backend startup failed: {str(e)}"
        
        # Run in background thread
        thread = threading.Thread(target=run_backend, daemon=True)
        thread.start()
    
    def check_devices(self):
        """Check backend status"""
        self.status = "🔍 Checking system status..."
        
        def check_devices_thread():
            try:
                # Get status from backend
                response = requests.get(f"{self.backend_url}/status", timeout=5)
                if response.status_code == 200:
                    self.status = "✅ System ready!"
                    # Start frontend
                    self.start_frontend()
                else:
                    self.status = "❌ Backend not responding"
                    
            except Exception as e:
                self.status = f"❌ Connection failed: {str(e)}"
                # Still try to start frontend
                self.start_frontend()
        
        thread = threading.Thread(target=check_devices_thread, daemon=True)
        thread.start()
    
    def start_frontend(self):
        """Start the CEVA frontend proxy"""
        self.status = "🌐 Starting CEVA Dashboard..."
        
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
                            self.launchReady = True
                            return
                    except:
                        pass
                
                self.status = "❌ Frontend startup timeout"
                
            except Exception as e:
                self.status = f"❌ Frontend startup failed: {str(e)}"
        
        thread = threading.Thread(target=run_frontend, daemon=True)
        thread.start()
    
    @Slot()
    def launchDashboard(self):
        """Launch the CEVA Dashboard in web browser"""
        try:
            webbrowser.open(self.frontend_url)
            self.status = "🚀 Opening CEVA Dashboard..."
        except Exception as e:
            self.status = f"❌ Failed to open browser: {str(e)}"


def main():
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Create backend checker
    backend_checker = BackendChecker()
    
    # Register with QML
    engine.rootContext().setContextProperty("backendChecker", backend_checker)
    
    # Load QML UI
    engine.load(QUrl("main_fixed.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    print("🚀 CEVA Launcher Ready.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
