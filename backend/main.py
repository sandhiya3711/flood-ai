from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Services
from services.weather_service import get_weather_data
from services.water_service import get_water_level
from ml.model import model_instance

load_dotenv()

app = FastAPI(title="Flood Forecast API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def read_root():
#     return {"message": "Flood Forecast System Backend Online", "status": "active"}

@app.get("/")
async def serve_root():
    """
    Explicitly serve the Next.js index.html at the root.
    """
    if os.path.exists(f"{STATIC_DIR}/index.html"):
        return FileResponse(f"{STATIC_DIR}/index.html")
    return {"error": "Frontend not found. Did you run 'npm run build'?"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/forecast")
def get_forecast(lat: float = 40.7128, lon: float = -74.0060):
    """
    Get flood forecast for a specific location.
    Defaults to New York Logic if not specified.
    """
    # 1. Fetch Data
    weather = get_weather_data(lat, lon)
    water = get_water_level()
    
    if not weather or not water:
        return {"error": "Failed to fetch environmental data"}
        
    # 2. Predict Risk
    # Using 12h rainfall heuristic estimate (4x 3h) + current level
    # Terrain and Drainage are mocked/constants for this MVP
    rainfall_val = weather.get("rainfall_3h", 0)
    water_val = water.get("water_level", 0)
    
    risk_level = model_instance.predict_risk(rainfall_val, water_val)
    
# ... (API routes above remain unchanged)

    return {
        "location": weather.get("location"),
        "risk_level": risk_level,
        "details": {
            "rainfall_3h_mm": rainfall_val,
            "river_water_level_ft": water_val,
            "soil_saturation": "High" if rainfall_val > 50 else "Normal"
        },
        "timestamp": weather.get("timestamp")
    }

# ---------------------------------------------------------
# Serve Frontend (Unified URL)
# ---------------------------------------------------------
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount static assets (Next.js export puts assets in _next/static, but plain 'out' has structure)
# Next.js 'out' folder usually acts as root.
STATIC_DIR = "../frontend-next/out"

# Check if build exists
if os.path.exists(STATIC_DIR):
    # Mount specific subdirectories if needed, or just rely on FileResponse for root
    # Next.js static export puts assets in `_next` folder.
    if os.path.exists(f"{STATIC_DIR}/_next"):
        app.mount("/_next", StaticFiles(directory=f"{STATIC_DIR}/_next"), name="next_assets")
    
    # Also serve generic assets if they exist (e.g. images)
    if os.path.exists(f"{STATIC_DIR}/assets"):
         app.mount("/assets", StaticFiles(directory=f"{STATIC_DIR}/assets"), name="assets")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """
    Serve the Next.js Static Export.
    """
    # 1. Check exact file match
    target_file = f"{STATIC_DIR}/{full_path}"
    if os.path.exists(target_file) and os.path.isfile(target_file):
        return FileResponse(target_file)
    
    # 2. Check HTML match (Next.js export: /about -> /about.html)
    target_html = f"{STATIC_DIR}/{full_path}.html"
    if os.path.exists(target_html) and os.path.isfile(target_html):
        return FileResponse(target_html)

    # 3. Default to index.html (SPA fallback, though strict static export might not need it if routing is handled via links)
    if os.path.exists(f"{STATIC_DIR}/index.html"):
        return FileResponse(f"{STATIC_DIR}/index.html")
        
    return {"error": "Frontend not built. Run 'npm run build' in frontend-next/ directory."}
