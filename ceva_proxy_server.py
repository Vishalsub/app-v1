#!/usr/bin/env python3
"""
CEVA Logistics Proxy Server
Serves the CEVA-branded frontend and proxies API calls to the original phosphobot backend.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import httpx
import uvicorn
import os
import asyncio

app = FastAPI(title="CEVA Logistics Robot Control", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Phosphobot backend URL
PHOSPHOBOT_BACKEND = "http://localhost:8080"

# Resolve paths relative to this file so it works on macOS/Linux/Jetson
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve static files from the CEVA-branded frontend (built dist)
ceva_dist_path = os.path.join(BASE_DIR, "cevalogistics-sg", "dashboard", "dist")
if os.path.exists(ceva_dist_path):
    app.mount("/assets", StaticFiles(directory=f"{ceva_dist_path}/assets"), name="assets")
    # Only mount static if it exists
    static_dir = f"{ceva_dist_path}/static"
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_ceva_dashboard():
    """Serve the CEVA-branded dashboard"""
    dashboard_path = os.path.join(ceva_dist_path, "index.html")
    
    if os.path.exists(dashboard_path):
        with open(dashboard_path, 'r') as f:
            content = f.read()
        return HTMLResponse(content=content)
    else:
        # Fallback: redirect to development server
        return RedirectResponse(url="http://localhost:5173")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def handle_routes(path: str, request: Request):
    """Handle both API calls and SPA routes"""
    
    # Skip static file routes
    if path.startswith(("assets/", "static/", "favicon.ico")):
        raise HTTPException(status_code=404, detail="Not found")
    
    # Check if this is an API call (has Accept: application/json or is a POST/PUT/PATCH/DELETE)
    is_api_call = (
        request.method in ["POST", "PUT", "PATCH", "DELETE"] or
        "application/json" in request.headers.get("accept", "") or
        path.startswith(("status", "api/", "admin/", "teleop/", "dataset/", "training/", "ai-control/", "files/", "update/", "torque/", "ws/", "video/", "frames/", "cameras/", "recording/", "joints/", "move/", "calibrate/", "gravity/", "robot/"))
    )
    
    if is_api_call:
        # Proxy API calls to the original phosphobot backend
        target_url = f"{PHOSPHOBOT_BACKEND}/{path}"
        
        # Get query parameters
        query_params = str(request.query_params) if request.query_params else ""
        if query_params:
            target_url += f"?{query_params}"
        
        try:
            async with httpx.AsyncClient() as client:
                # Get request body if it exists
                body = None
                if request.method in ["POST", "PUT", "PATCH"]:
                    body = await request.body()
                
                # Forward the request
                response = await client.request(
                    method=request.method,
                    url=target_url,
                    headers=dict(request.headers),
                    content=body,
                    timeout=30.0
                )
                
                # Return the response
                return response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
                
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Backend connection error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Proxy error: {str(e)}")
    else:
        # Serve SPA routes for the CEVA dashboard
        dashboard_path = os.path.join(ceva_dist_path, "index.html")
        
        if os.path.exists(dashboard_path):
            with open(dashboard_path, 'r') as f:
                content = f.read()
            return HTMLResponse(content=content)
        else:
            return RedirectResponse(url=f"http://localhost:5173/{path}")

if __name__ == "__main__":
    print("🚀 Starting CEVA Logistics Proxy Server...")
    print("📡 CEVA Dashboard will be available at: http://localhost:3000")
    print("🔗 Proxying API calls to phosphobot backend at: http://localhost:8080")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=3000,
        log_level="info"
    )
