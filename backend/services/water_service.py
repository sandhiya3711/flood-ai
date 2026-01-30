import random

def get_water_level(station_id="mock_station"):
    """
    Fetches real water level or generates mock data.
    """
    # In a real app, we would query USGS Water Services here
    # For this prototype, we return a mock value
    
    # Random water level between 2ft and 25ft
    # Thresholds: Low < 10, Moderate < 18, High < 24, Critical > 24
    
    current_level = round(random.uniform(5, 26), 2)
    
    return {
        "station_id": station_id,
        "water_level": current_level,
        "unit": "ft",
        "status": "active"
    }
