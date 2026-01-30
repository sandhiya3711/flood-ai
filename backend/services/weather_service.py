import os
import requests
import random
from datetime import datetime

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_data(lat, lon):
    """
    Fetches real weather data or generates mock data if no key is present.
    """
    if not OPENWEATHER_API_KEY:
        # Mock Data Generation
        print("Using Mock Weather Data")
        return {
            "rainfall_1h": round(random.uniform(0, 50), 2),  # mm
            "rainfall_3h": round(random.uniform(0, 120), 2), # mm
            "location": "Mock City",
            "timestamp": datetime.now().isoformat()
        }
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Extract rainfall (if available, often in 'rain' object)
        rain = data.get('rain', {})
        rainfall_1h = rain.get('1h', 0)
        rainfall_3h = rain.get('3h', 0)
        
        return {
            "rainfall_1h": rainfall_1h,
            "rainfall_3h": rainfall_3h,
            "location": data.get('name', 'Unknown'),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None
