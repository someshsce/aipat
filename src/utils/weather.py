import os
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper

env_path = os.path.join(os.path.expanduser("~"), ".aipat.env")
load_dotenv(env_path)

OPENWEATHERMAP_API_KEY=os.getenv("OPENWEATHERMAP_API_KEY")

def get_weather(location):
    weather = OpenWeatherMapAPIWrapper()
    weather_data = weather.run(location)
    return weather_data

weather_tool = Tool(
    name="Weather",
    func= get_weather,
    description="Fetches real-time weather information for a given location."
)
