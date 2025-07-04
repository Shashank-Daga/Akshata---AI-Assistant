import requests

WEATHER_API_KEY = ""


def get_weather_info(query):
    try:
        city = query.lower().split("weather in")[-1].strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()

        if res.get("cod") != 200:
            return f"City {city} not found."

        temp = res['main']['temp']
        condition = res['weather'][0]['description']
        humidity = res['main']['humidity']
        return f"The weather in {city} is {condition} with {temp} degree celcius temperature and {humidity}% humidity."

    except Exception as e:
        return "Failed to fetch weather data."
