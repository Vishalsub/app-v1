# cevalogistics-sg

A customized fork of [phosphobot](https://github.com/phospho-app/phosphobot) with the same frontend and backend, branded for CEVA Logistics Singapore.  
This dashboard enables robot control, dataset recording, and AI model training — all from the repp

---

## Features
- **Control Robot** – Use keyboard, leader arm, or VR headset.
- **Record & Replay** – Store datasets and replay movements.
- **AI Training** – Train new skills directly from your recorded data.
- **AI Control** – Deploy and run trained AI models.
- **Advanced Settings** – Admin config, API docs, camera overview, and network management.

---

## Installation

### macOS & Linux
Open a terminal and run:

```bash
curl -fsSL https://raw.githubusercontent.com/your-org/cevalogistics-sg/main/install.sh | bash


Usage
After installation, start the server with:
cevalogistics-sg run
The server may take up to 15 seconds to initialize.
Open your browser and navigate to:
http://localhost:80
You will see the CEVA Logistics dashboard (based on phosphobot).

Development Setup
If you want to run in dev mode:
git clone https://github.com/your-org/cevalogistics-sg.git
cd cevalogistics-sg
uv sync
uv run cevalogistics-sg
Notes
The only difference from phosphobot is branding (name + logo).
Executable renamed from phosphobot to:
cevalogistics-sg


- Repo name: `cevalogistics-sg` (forked from `phosphobot`)  
- Executable must run as: `cevalogistics-sg run`  
- Replace all branding `phosphobot` → `cevalogistics-sg`  
- Keep frontend/backend identical.  
- Add my company logo instead of phospho.  
- Installation script must match README instructions.


my company logo : /Users/vishal/Documents/Projects/app/new/CEVA_Logo_Blue_HR.jpg



 I made the launcher Linux-friendly:
main_fixed.qml logo now uses a relative path (CEVA_Logo_Blue_HR.jpg)
ceva_proxy_server.py now resolves cevalogistics-sg/dashboard/dist relative to the script (no macOS paths)
Do this on your Jetson Nano (Ubuntu-based):
1) System packages
sudo apt update
sudo apt install -y python3-venv python3-pip pipx \
  libgl1 libegl1 libxkbcommon0 libxkbcommon-x11-0 libxcb-render0 libxcb-xfixes0 \
  gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-libav
2) Permissions (serial + cameras)
sudo usermod -aG dialout $USER
sudo usermod -aG video $USER
# log out/in (or reboot) after this step
3) Install phosphobot (backend) with pipx
pipx ensurepath
pipx install phosphobot
# reopen terminal so PATH is updated, or:
export PATH="$HOME/.local/bin:$PATH"
"
4) Launch the CEVA launcher (uses its own venv)

cd /path/to/new   # the folder you copied
chmod +x run_launcher.sh
./run_launcher.sh
sh
This creates launcher_env venv on first run and installs PySide6, requests, fastapi, uvicorn, httpx.
Backend runs on http://127.0.0.1:8080
Proxy serves CEVA frontend on http://127.0.0.1:3000
Click “Launch Dashboard” to open the browser.
5) If GUI doesn’t work on Nano, use CLI launcher

source launcher_env/bin/activate
python3 test_system.py
# It will start backend + proxy and open http://localhost:3000
Notes:
Ensure cevalogistics-sg/dashboard/dist exists on the Nano (it should be in your copied folder). If it’s missing, build it on a machine with Node and copy the dist/ over.
If camera preview returns 502 in the dashboard, install the GStreamer packages above and replug the cameras.
That’s it. Try step 4 now; if anything fails, tell me the exact error text and I’ll fix it
