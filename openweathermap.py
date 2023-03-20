import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["API_KEY"]


def get_weather_data(url):
    """
    Fetches weather data from OpenWeatherMap API.

    Args:
        url (str): The URL of the API endpoint.

    Returns:
        dict: A dictionary containing the weather data.

    Raises:
        requests.exceptions.HTTPError: If the API request returns an error.

    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["cod"] != 200:
            raise requests.exceptions.HTTPError(
                f"Error {data['cod']}: {data['message']}"
            )
        return data
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.HTTPError(
            f"Error connecting to API: {e}"
        ) from e


def get_weather_info(data):
    weather = data["weather"][0]["description"].capitalize()
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    return weather, temperature, humidity, wind_speed


def print_weather_info(city, weather, temperature, humidity, wind_speed):
    print(f"The weather in {city} is {weather}.")
    print(f"The temperature is {temperature:.1f}°C.")
    print(f"The humidity is {humidity}%.")
    print(f"The wind speed is {wind_speed:.1f} m/s.")


if __name__ == "__main__":
    CITY = "London"
    UNITS = "metric"
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&units={UNITS}&appid={API_KEY}"
    try:
        weather_data = get_weather_data(URL)
        weather_info = get_weather_info(weather_data)
        print_weather_info(CITY, *weather_info)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")

    except Exception as e:
        print(f"Error occurred: {e}")
