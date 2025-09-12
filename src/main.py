"""A simple morning bot that greets the user and provides current weather information based on their location.
"""

from weather import get_weather
from news import get_domestic_news, get_international_news, NewsAPIError
import geocoder

def get_location():
    g = geocoder.ip('me')
    return g.city

def greet_user():
    message = "Good Morning!"
    print(message)

def print_weather(location):
    weather = get_weather(location)
    temperature = weather.get("temperature")
    condition = weather.get("weather")
    print(f"The current temperature in {location} is {temperature}°C with {condition}.")

def print_news():
    domestic_news = get_domestic_news()
    print("Here are the latest domestic news headlines:")
    for idx, article in enumerate(domestic_news, start=1):
        print(f"{idx}. {article}")
    print("\n")
    international_news = get_international_news()
    print("Here are the latest international news headlines:")
    for idx, article in enumerate(international_news, start=1):
        print(f"{idx}. {article}")

if __name__ == "__main__":
    try:
        greet_user()
        print("\n")
        location = get_location()
        print_weather(location)
        print("\n")
        print_news()
    except NewsAPIError as e:
        print(f"Could not provide news updates: {str(e)}")

