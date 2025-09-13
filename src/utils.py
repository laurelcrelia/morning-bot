"""
Utility functions for the morning bot.
"""

import geocoder

def get_location() -> str:
    g = geocoder.ip('me')
    return g.city