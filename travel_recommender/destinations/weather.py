import os
import requests
from django.conf import settings
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def get_weather_data(city, country):
    """Fetch current weather data from OpenWeatherMap API"""
    api_key = settings.WEATHER_API_KEY
    if not api_key:
        return None
    
    try:
        # First try to get coordinates for the city
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        if not geo_data:
            return None
            
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        
        # Then get weather data
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        if weather_response.status_code != 200:
            return None
            
        return {
            'weather': weather_data['weather'][0]['description'].title(),
            'temperature': weather_data['main']['temp'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'icon': weather_data['weather'][0]['icon']
        }
    except Exception as e:
        logger.error(f"Error fetching weather data for {city}, {country}: {e}")
        return None