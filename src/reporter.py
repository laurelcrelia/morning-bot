"""Reporter module to handle greetings, weather, and news reporting."""

from weather import get_weather
from news import News, NewsAPIError

def greet_user() -> None:
    message = "Good Morning!"
    print(message)

def report_weather(location: str) -> None:
    weather = get_weather(location)
    temperature = weather.get("temperature")
    condition = weather.get("weather")
    print(f"The current temperature in {location} is {temperature}°C with {condition}.")

def report_news() -> None:
    try:
        news_api = News()
        domestic_news = news_api.get_domestic_news()
        international_news = news_api.get_international_news()
        print("Here are the latest domestic news headlines:")
        for idx, article in enumerate(domestic_news, start=1):
            print(f"{idx}. {article}")
        print("\n")
        print("Here are the latest international news headlines:")
        for idx, article in enumerate(international_news, start=1):
            print(f"{idx}. {article}")
    except NewsAPIError as e:
        print(f"Could not provide news updates: {str(e)}")