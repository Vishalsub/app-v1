#!/usr/bin/env python3
"""
Test script to verify backend connection and device detection
"""

import requests
import json

def test_backend():
    backend_url = "http://localhost:8080"
    
    try:
        print("🔍 Testing backend connection...")
        response = requests.get(f"{backend_url}/status", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Count robots
            robots = data.get('robots', [])
            robot_count = len(robots)
            
            # Count cameras
            cameras_data = data.get('cameras', {})
            cameras = cameras_data.get('cameras_status', [])
            camera_count = len(cameras)
            
            print(f"✅ Backend is running!")
            print(f"🤖 Robots detected: {robot_count}")
            print(f"📷 Cameras detected: {camera_count}")
            
            if robot_count > 0:
                print(f"   Robot names: {robots}")
            
            if camera_count > 0:
                active_cameras = [c for c in cameras if c.get('is_active', False)]
                print(f"   Active cameras: {len(active_cameras)}")
            
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_backend()
