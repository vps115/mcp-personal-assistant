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
        print(data)
        
        # Extract weather information
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        desc = data["weather"][0]["description"]
        city_name = data["name"]
        wind_speed = data["wind"]["speed"]
        visibility = data.get("visibility", "N/A")
        
        # Format the weather information
        weather_info = f"""
🌍 Weather in {city_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌡  Temperature: {temp}°C
🔥 Feels like: {feels_like}°C
💧 Humidity: {humidity}%
🌪  Wind Speed: {wind_speed} m/s
👁  Visibility: {visibility} meters
🌤  Conditions: {desc.title()}
📊 Pressure: {pressure} hPa
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return weather_info
    except requests.exceptions.HTTPError as err:
        return f"Weather API error: {err}"
    except Exception as e:
        return f"Failed to fetch weather: {e}"
