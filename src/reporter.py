"""Reporter module to handle greetings, weather, and news reporting."""

from weather import get_weather
from news import News, NewsAPIError

def greet_user() -> str:
    message = "Good Morning!"
    return message

def report_weather(location: str) -> str:
    weather = get_weather(location)
    temperature = weather.get("temperature")
    condition = weather.get("weather")
    message = f"The current temperature in {location} is {temperature}°C with {condition}."
    return message

def report_news() -> str:
    try:
        news_api = News()
        domestic_news = news_api.get_domestic_news()
        international_news = news_api.get_international_news()
        
        message = "Here are the latest domestic news headlines:\n"
        for idx, article in enumerate(domestic_news, start=1):
            message += f"{idx}. {article}\n"
        
        message += "\nHere are the latest international news headlines:\n"
        for idx, article in enumerate(international_news, start=1):
            message += f"{idx}. {article}\n"
        
        return message
    except NewsAPIError as e:
        error_message = f"Could not provide news updates: {str(e)}"
        print(error_message)
        return error_message