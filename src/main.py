"""A simple morning bot that greets the user and provides current weather information based on their location.
"""

from weather import get_weather
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

if __name__ == "__main__":
    greet_user()
    location = get_location()
    print_weather(location)
