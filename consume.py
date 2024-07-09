import streamlit as st
from kafka import KafkaConsumer
import json
from environment import KAFKA_BROKER, KAFKA_TOPIC, KAFKA_GROUP_ID

def get_weather_data_from_kafka():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in consumer:
        yield message.value

def main():
    st.title("Weather Data Consumer Dashboard")
    st.write("Real-time weather data from Kafka topic:")
    
    weather_data_stream = get_weather_data_from_kafka()
    
    for weather_data in weather_data_stream:
        st.write(weather_data)

if __name__ == "__main__":
    main()
