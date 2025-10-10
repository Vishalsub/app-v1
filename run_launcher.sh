#!/bin/bash

echo "🚀 Starting CEVA Logistics Launcher..."

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Check if virtual environment exists, if not create it
if [ ! -d "launcher_env" ]; then
    echo "📋 Creating virtual environment..."
    python3 -m venv launcher_env
    echo "📦 Installing dependencies..."
    source launcher_env/bin/activate
    pip install PySide6 requests fastapi uvicorn httpx
else
    echo "📦 Activating virtual environment..."
    source launcher_env/bin/activate
fi

    # Run the launcher
    echo "🎯 Launching CEVA Launcher..."
    python ceva_launcher_fixed.py
