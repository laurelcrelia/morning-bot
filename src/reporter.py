"""Reporter module to handle greetings, weather, and news reporting."""

import os
import datetime
from zoneinfo import ZoneInfo
from weather import get_weather
from news import News, NewsAPIError

def get_current_hour() -> int:
    """Get current hour in user's timezone."""
    timezone = os.getenv("USER_TIMEZONE", "UTC")
    try:
        tz = ZoneInfo(timezone)
        return datetime.datetime.now(tz).hour
    except Exception:
        # Fallback to UTC if timezone is invalid
        return datetime.datetime.now(ZoneInfo("UTC")).hour

def get_weather_emoji(condition: str, temperature: float) -> str:
    """Return an appropriate emoji based on weather condition."""
    condition_lower = condition.lower()
    
    if "clear" in condition_lower or "sunny" in condition_lower:
        return "☀️"
    elif "partly cloudy" in condition_lower:
        return "🌤️"
    elif "cloud" in condition_lower or "overcast" in condition_lower:
        return "☁️"
    elif "thunder" in condition_lower:
        return "⛈️"
    elif "rain" in condition_lower or "drizzle" in condition_lower:
        return "🌧️"
    elif "snow" in condition_lower or "blizzard" in condition_lower or "sleet" in condition_lower:
        return "🌨️"
    elif "storm" in condition_lower:
        return "🌊"
    elif "fog" in condition_lower or "mist" in condition_lower:
        return "🌫️"
    elif "wind" in condition_lower:
        return "💨"
    else:
        return "🌡️"

def get_greeting_emoji() -> str:
    """Return time-appropriate greeting emoji."""
    hour = get_current_hour()
    if 5 <= hour < 12:
        return "☀️"
    elif 12 <= hour < 18:
        return "🌤️"
    else:
        return "🌙"

def greet_user() -> str:
    hour = get_current_hour()
    
    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    elif 18 <= hour < 22:
        greeting = "Good Evening"
    else:
        greeting = "Hello"
    
    emoji = get_greeting_emoji()
    message = f"{emoji} *{greeting}!* {emoji}"
    return message

def report_weather(location: str) -> str:
    weather = get_weather(location)
    temperature = weather.get("temperature")
    condition = weather.get("weather")
    
    weather_emoji = get_weather_emoji(condition, temperature)
    
    if temperature < -5:
        temp_emoji = "🥶"
    elif temperature < 0:
        temp_emoji = "❄️"
    elif temperature < 10:
        temp_emoji = "🧥"
    elif temperature < 20:
        temp_emoji = "😊"
    elif temperature < 30:
        temp_emoji = "🌡️"
    else:
        temp_emoji = "🔥"
    
    message = f"📍 *Weather in {location}*\n"
    message += f"{weather_emoji} {condition}\n"
    message += f"{temp_emoji} Temperature: *{temperature}°C*"
    
    return message

def report_news() -> str:
    try:
        news_api = News()
        domestic_news = news_api.get_domestic_news()
        international_news = news_api.get_international_news()
        
        message = "📰 *Domestic News Headlines*\n"
        message += "━━━━━━━━━━━━━━━━━━\n"
        for idx, article in enumerate(domestic_news, start=1):
            message += f"▪️ {article}\n"
        
        message += "\n🌍 *International News Headlines*\n"
        message += "━━━━━━━━━━━━━━━━━━\n"
        for idx, article in enumerate(international_news, start=1):
            message += f"▪️ {article}\n"
        
        return message
    except NewsAPIError as e:
        error_message = f"❌ Could not provide news updates: {str(e)}"
        print(error_message)
        return error_message