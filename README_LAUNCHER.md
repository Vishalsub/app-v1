# CEVA Logistics Launcher

This is a PySide6-based launcher application for the CEVA Logistics phosphobot system.

## Quick Start

### Option 1: PySide6 Launcher (GUI)
```bash
./run_launcher.sh
```

### Option 2: Automatic Test & Launch
```bash
python3 test_system.py
```

### Option 3: Manual Launch
```bash
# Terminal 1: Start backend
phosphobot run --port=8080 --host=127.0.0.1 --no-telemetry

# Terminal 2: Start frontend
python3 ceva_proxy_server.py

# Open browser to: http://localhost:3000
```

## What Each Option Does

### PySide6 Launcher (`./run_launcher.sh`)
- Beautiful GUI with CEVA branding
- Shows real-time status updates
- Displays robot and camera counts
- Automatically starts backend and frontend
- Click "Launch Dashboard" to open web browser

### Test System (`python3 test_system.py`)
- Command-line interface
- Automatically starts backend and frontend if needed
- Opens CEVA Dashboard in browser automatically
- Shows system status

### Manual Launch
- Full control over each component
- Good for debugging
- Run each command in separate terminals

## System Requirements

- Python 3.8+
- PySide6 (for GUI launcher)
- phosphobot (installed via pipx)
- FastAPI, uvicorn, httpx (for proxy server)

## Troubleshooting

### Backend Issues
- Make sure robots are connected via USB
- Check that phosphobot is installed: `which phosphobot`
- Restart backend: `pkill phosphobot`

### Frontend Issues
- Check if port 3000 is available
- Restart proxy server: `pkill -f ceva_proxy_server`

### Launcher Issues
- Install dependencies: `pip install PySide6 requests fastapi uvicorn httpx`
- Check virtual environment: `source launcher_env/bin/activate`

## URLs

- **CEVA Dashboard**: http://localhost:3000
- **Phosphobot Backend**: http://localhost:8080
- **API Status**: http://localhost:8080/status
