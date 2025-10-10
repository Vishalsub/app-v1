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