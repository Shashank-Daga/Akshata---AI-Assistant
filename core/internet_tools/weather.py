import os
import json
import requests


# Loading API Key safely
def load_api_key():
    config_path = "config/settings.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError("Missing config/settings.json file with your Weather API key.")

    with open(config_path, "r") as f:
        config = json.load(f)

    apiKey = config.get("WEATHER_API_KEY")
    if not apiKey:
        raise ValueError("Weather API key not found in settings.json.")
    return apiKey


WEATHER_API_KEY = load_api_key()


def get_weather_info(query):
    try:
        if "weather in" in query.lower():
            city = query.lower().split("weather in")[-1].strip()
        else:
            return "Please specify a city, like 'weather in Mumbai'."

        if not WEATHER_API_KEY:
            return "Weather API key not set."

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()

        if res.get("cod") != 200:
            return f"City '{city}' not found."

        temp = res['main']['temp']
        condition = res['weather'][0]['description']
        humidity = res['main']['humidity']
        return f"The weather in {city} is {condition} with {temp}°C temperature and {humidity}% humidity."

    except Exception:
        return "Failed to fetch weather data."
