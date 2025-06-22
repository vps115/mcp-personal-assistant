import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str = "Delhi", units: str = "metric") -> str:
    if not API_KEY:
        return "Weather API key not found."

    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units={}'.format(city, API_KEY, "metric")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        city_name = data["name"]

        return f"{city_name}: {temp}°C, {desc}"
    except requests.exceptions.HTTPError as err:
        return f"Weather API error: {err}"
    except Exception as e:
        return f"Failed to fetch weather: {e}"
