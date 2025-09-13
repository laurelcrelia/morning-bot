"""Main module to greet the user, provide weather updates, and news headlines."""

from utils import get_location
from reporter import greet_user, report_weather, report_news

def main() -> None:
    greet_user()
    print("\n")
    location = get_location()
    report_weather(location)
    print("\n")
    report_news()

if __name__ == "__main__":
    main()

