"""Weather Tool - Returns hardcoded weather information for any city."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def get_weather(city: str) -> str:
    """
    Get weather information for a given city.
    
    Args:
        city: Name of the city
        
    Returns:
        Weather information as a string
    """
    # Hardcoded weather data
    weather_data = {
        "temperature": "22°C",
        "condition": "Partly Cloudy",
        "humidity": "65%",
        "wind_speed": "15 km/h"
    }
    
    return f"Weather in {city}: {weather_data['condition']}, Temperature: {weather_data['temperature']}, Humidity: {weather_data['humidity']}, Wind Speed: {weather_data['wind_speed']}"


def create_weather_tool() -> Any:
    """
    Create and return the weather tool.
    
    Returns:
        A tool that can be used by the agent to get weather information
    """
    tool = get_weather
    
    logger.info("Weather tool created successfully")
    return tool
