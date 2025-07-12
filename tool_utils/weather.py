import logging
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str = "Delhi", units: str = "metric") -> dict:
    """Get weather information for a city.
    
    Args:
        city (str): City name
        units (str): Units (metric/imperial)
        
    Returns:
        dict: Weather information or error message
        
    Raises:
        ValueError: If API key is missing
        requests.RequestException: If API call fails
    """
    if not API_KEY:
        logger.error("OpenWeather API key not found in environment variables")
        raise ValueError("OpenWeather API key not found. Please set OPENWEATHER_API_KEY in .env")

    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}'
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200 or 'cod' in data and data['cod'] != 200:
            error_msg = data.get('message', 'Unknown error')
            logger.error(f"OpenWeather API error: {error_msg}")
            return f"Weather service error: {error_msg}"
        
        # Extract weather information with safe get operations
        main_data = data.get("main", {})
        weather_data = data.get("weather", [{}])[0]
        temp = main_data.get("temp", "N/A")
        feels_like = main_data.get("feels_like", "N/A")
        humidity = main_data.get("humidity", "N/A")
        pressure = main_data.get("pressure", "N/A")
        desc = weather_data.get("description", "N/A")
        city_name = data.get("name", city)
        wind = data.get("wind", {})
        wind_speed = wind.get("speed", "N/A")
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
🌤  Conditions: {desc.title() if desc != 'N/A' else desc}
📊 Pressure: {pressure} hPa
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return weather_info
    except requests.exceptions.HTTPError as err:
        return f"Weather API error: {err}"
    except Exception as e:
        return f"Failed to fetch weather: {e}"
