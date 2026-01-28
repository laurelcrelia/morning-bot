"""
Utility functions for the morning bot.
"""
import geocoder
import os
from dotenv import load_dotenv

load_dotenv()

def get_location() -> str:
    """Get user location from environment variable or IP geolocation fallback."""
    # First try to get from environment variable (works on Cloud Functions)
    location = os.getenv("USER_LOCATION")
    if location:
        return location
    
    # Fallback to IP-based geolocation for local runs
    try:
        import geocoder
        g = geocoder.ip('me')
        return g.city if g.city else "Unknown"
    except Exception:
        return "Unknown"
