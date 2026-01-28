"""Cloud Functions entry point for morning-bot."""

import sys
import os
import functions_framework

# Add src directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import get_location
from reporter import greet_user, report_weather, report_news
from telegram_sender import send_telegram_message


@functions_framework.http
def morning_briefing(request):
    """HTTP Cloud Function that sends the morning briefing to Telegram.
    
    Args:
        request (flask.Request): The request object.
    
    Returns:
        A JSON response with status.
    """
    try:
        greeting = greet_user()
        location = get_location()
        weather_report = report_weather(location)
        news_report = report_news()
        
        telegram_message = f"{greeting}\n\n{weather_report}\n\n{news_report}"
        send_telegram_message(telegram_message)
        
        return {
            "status": "success",
            "message": "Morning briefing sent to Telegram"
        }, 200
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500
