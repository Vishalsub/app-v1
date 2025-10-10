#!/usr/bin/env python3
"""
CEVA Logistics Launcher - Auto-launch version
"""

import requests
import webbrowser
import subprocess
import time
import sys
import os

def check_backend():
    """Check if phosphobot backend is running"""
    try:
        response = requests.get("http://localhost:8080/status", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_device_counts():
    """Get robot and camera counts"""
    try:
        response = requests.get("http://localhost:8080/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Count robots
            robots = data.get('robots', [])
            robot_count = len(robots)
            
            # Count cameras
            cameras_data = data.get('cameras', {})
            cameras = cameras_data.get('cameras_status', [])
            camera_count = len(cameras)
            
            return robot_count, camera_count
    except:
        pass
    return 0, 0

def start_backend():
    """Start phosphobot backend"""
    print("🚀 Starting phosphobot backend...")
    try:
        process = subprocess.Popen([
            "phosphobot", "run", 
            "--port=8080", 
            "--host=127.0.0.1", 
            "--no-telemetry"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for backend to start
        max_wait = 30
        for i in range(max_wait):
            time.sleep(1)
            print(f"⏳ Starting backend... ({i+1}/{max_wait})")
            
            if check_backend():
                print("✅ Backend started successfully!")
                return True
        
        print("❌ Backend startup timeout")
        return False
        
    except Exception as e:
        print(f"❌ Backend startup failed: {str(e)}")
        return False

def start_frontend():
    """Start CEVA frontend proxy"""
    print("🌐 Starting CEVA Dashboard...")
    try:
        # Check if already running
        try:
            response = requests.get("http://localhost:3000", timeout=2)
            if response.status_code == 200:
                print("✅ CEVA Dashboard already running!")
                return True
        except:
            pass
        
        process = subprocess.Popen([
            "python3", "ceva_proxy_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for frontend to start
        max_wait = 10
        for i in range(max_wait):
            time.sleep(1)
            try:
                response = requests.get("http://localhost:3000", timeout=2)
                if response.status_code == 200:
                    print("✅ CEVA Dashboard ready!")
                    return True
            except:
                pass
        
        print("❌ Frontend startup timeout")
        return False
        
    except Exception as e:
        print(f"❌ Frontend startup failed: {str(e)}")
        return False

def main():
    print("🚀 CEVA Logistics Launcher")
    print("=" * 40)
    
    # Check backend
    if not check_backend():
        print("🔍 Backend not running, starting...")
        if not start_backend():
            print("❌ Failed to start backend")
            return
    else:
        print("✅ Backend already running!")
    
    # Check devices
    print("🔍 Detecting robots and cameras...")
    robot_count, camera_count = get_device_counts()
    
    if robot_count > 0 and camera_count > 0:
        print(f"✅ Found {robot_count} robots and {camera_count} cameras!")
    elif robot_count > 0:
        print(f"✅ Found {robot_count} robots!")
    elif camera_count > 0:
        print(f"✅ Found {camera_count} cameras!")
    else:
        print("⚠️ No robots or cameras detected")
    
    # Start frontend
    if start_frontend():
        print("\n🎯 Launching CEVA Dashboard...")
        
        try:
            webbrowser.open("http://localhost:3000")
            print("🚀 CEVA Dashboard opened in browser!")
            print("🌐 URL: http://localhost:3000")
        except Exception as e:
            print(f"❌ Failed to open browser: {str(e)}")
            print("🌐 Please open http://localhost:3000 in your browser manually")
    else:
        print("❌ Failed to start frontend")

if __name__ == "__main__":
    main()
