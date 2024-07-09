import streamlit as st
from environment import WEATHER_API_KEY, KAFKA_BROKER, KAFKA_TOPIC
from kafka import KafkaProducer
import requests
import json

def fetch_weather_data(city_name):
    search_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={WEATHER_API_KEY}&q={city_name}"
    search_response = requests.get(search_url)
    search_result = search_response.json()[0]
    city_key = search_result['Key']
    
    weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{city_key}?apikey={WEATHER_API_KEY}"
    weather_response = requests.get(weather_url)
    weather_info = weather_response.json()[0]
    
    return weather_info

def main():
    st.title("Weather Data Producer Dashboard")
    city_name = st.text_input("Enter a city name:")
    
    if st.button("Fetch and Send Weather Data"):
        weather_data = fetch_weather_data(city_name)

        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        producer.send(KAFKA_TOPIC, weather_data)
        producer.flush()
        
        st.success(f"Weather data for {city_name} has been sent to Kafka topic '{KAFKA_TOPIC}'.")

if __name__ == "__main__":
    main()
