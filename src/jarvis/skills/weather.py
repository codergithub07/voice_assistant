"""Weather skill using OpenWeatherMap API."""
import os
import requests
from typing import Optional
from jarvis.config import OPENWEATHER_API_KEY, OPENWEATHER_DEFAULT_CITY

class WeatherSkill:
    """Fetches real-time weather information."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or OPENWEATHER_API_KEY or os.getenv("OPENWEATHER_API_KEY", "")

    def get_weather(self, city: Optional[str] = None) -> str:
        """Fetch current weather for city."""
        target_city = city or OPENWEATHER_DEFAULT_CITY
        if not self.api_key:
            return "OpenWeatherMap API key is not configured. Please set OPENWEATHER_API_KEY in .env."

        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": target_city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                desc = data["weather"][0]["description"]
                city_name = data.get("name", target_city)
                return f"In {city_name}, it is currently {temp}°C with {desc}, feels like {feels_like}°C."
            elif response.status_code == 401:
                return "Invalid OpenWeatherMap API key."
            elif response.status_code == 404:
                return f"Could not find weather data for city '{target_city}'."
            else:
                return f"Unable to fetch weather, status code {response.status_code}."
        except requests.RequestException as e:
            return f"Weather service network error: {e}"
