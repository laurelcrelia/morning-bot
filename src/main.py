"""Main module to greet the user, provide weather updates, and news headlines."""

from utils import get_location
from reporter import greet_user, report_weather, report_news
from telegram_sender import send_telegram_message

def main() -> None:
    # Test Telegram integration
    send_telegram_message("Hello World")
    
    greet_user()
    print("\n")
    location = get_location()
    report_weather(location)
    print("\n")
    report_news()

if __name__ == "__main__":
    main()

