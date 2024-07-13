import requests
from environment import WEATHER_API_KEY

def fetch_location_key(city_name):
    search_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={WEATHER_API_KEY}&q={city_name}"
    response = requests.get(search_url)
    location_data = response.json()[0]
    return location_data['Key']

def fetch_current_weather(location_key):
    weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={WEATHER_API_KEY}"
    response = requests.get(weather_url)
    weather_info = response.json()[0]
    return weather_info

def fetch_weather_data(city_name):
    location_key = fetch_location_key(city_name)
    weather_data = fetch_current_weather(location_key)
    return weather_data
