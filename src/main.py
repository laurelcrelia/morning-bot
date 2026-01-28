"""Main module to greet the user, provide weather updates, and news headlines."""

from utils import get_location
from reporter import greet_user, report_weather, report_news
from telegram_sender import send_telegram_message

def main() -> None:
    greeting = greet_user()
    
    location = get_location()
    weather_report = report_weather(location)
    
    news_report = report_news()
    
    telegram_message = f"{greeting}\n\n{weather_report}\n\n{news_report}"
    send_telegram_message(telegram_message)

if __name__ == "__main__":
    main()

