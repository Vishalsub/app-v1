#!/usr/bin/env python3
"""
Test script to verify the CEVA system is working
"""

import requests
import webbrowser
import subprocess
import time
import sys

def test_backend():
    """Test if phosphobot backend is running"""
    try:
        response = requests.get("http://localhost:8080/status", timeout=2)
        if response.status_code == 200:
            data = response.json()
            robots = data.get('robots', [])
            cameras = data.get('cameras', {}).get('video_cameras_ids', [])
            print(f"✅ Backend running: {len(robots)} robots, {len(cameras)} cameras")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running")
        return False
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return False

def test_frontend():
    """Test if CEVA frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=2)
        if response.status_code == 200:
            print("✅ CEVA Frontend running")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend not running")
        return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False

def start_backend():
    """Start phosphobot backend"""
    print("🚀 Starting phosphobot backend...")
    try:
        subprocess.Popen([
            "phosphobot", "run", 
            "--port=8080", 
            "--host=127.0.0.1", 
            "--no-telemetry"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for backend to start
        for i in range(30):
            time.sleep(1)
            if test_backend():
                return True
            print(f"⏳ Waiting for backend... ({i+1}/30)")
        
        print("❌ Backend startup timeout")
        return False
    except Exception as e:
        print(f"❌ Backend startup failed: {e}")
        return False

def start_frontend():
    """Start CEVA frontend"""
    print("🌐 Starting CEVA Dashboard...")
    try:
        subprocess.Popen([
            "python3", "ceva_proxy_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for frontend to start
        for i in range(10):
            time.sleep(1)
            if test_frontend():
                return True
            print(f"⏳ Waiting for frontend... ({i+1}/10)")
        
        print("❌ Frontend startup timeout")
        return False
    except Exception as e:
        print(f"❌ Frontend startup failed: {e}")
        return False

def main():
    print("🔍 Testing CEVA Logistics System...")
    print("=" * 50)
    
    # Test backend
    if not test_backend():
        if not start_backend():
            print("❌ Failed to start backend")
            sys.exit(1)
    
    # Test frontend
    if not test_frontend():
        if not start_frontend():
            print("❌ Failed to start frontend")
            sys.exit(1)
    
    print("\n✅ System ready!")
    print("🌐 Opening CEVA Dashboard...")
    
    # Open browser
    try:
        webbrowser.open("http://localhost:3000")
        print("🚀 CEVA Dashboard opened in browser!")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print("🌐 Please manually open: http://localhost:3000")

if __name__ == "__main__":
    main()
