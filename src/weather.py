"""Get the current weather for a specific location."""

import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_weather(location):
    try:
        # location = get_coordinates(location)
        url = f"https://api.weatherapi.com/v1/current.json?key={os.getenv('WEATHER_API_KEY')}&q={location}&aqi=no"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            return_data = {
                "location": data["location"]["name"],
                "temperature": data["current"]["temp_c"],
                "weather": data["current"]["condition"]["text"]
            }
            return return_data
        else:
            raise Exception(f"Error fetching weather data: {response.status_code}")
    except Exception as e:
        return {"Unable to retrieve weather data": str(e)}
