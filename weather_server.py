# math_server.py
...

# weather_server.py
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

app = FastAPI()
mcp = FastMCP("Weather")
#mcp.settings.port = 8000

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    # Mock weather data for different locations
    weather_data = {
        "new york": "Sunny, 72°F",
        "london": "Rainy, 60°F",
        "tokyo": "Cloudy, 65°F",
        "paris": "Partly cloudy, 68°F"
    }
    
    location = location.lower()
    if "weather" in location:
        # Extract location from query
        for city in weather_data.keys():
            if city in location:
                return f"The weather in {city.title()} is {weather_data[city]}"
        return "Please specify a city name in your query."
    return weather_data.get(location, "Weather data not available for this location.")

if __name__ == "__main__":
    mcp.run(transport="sse")



