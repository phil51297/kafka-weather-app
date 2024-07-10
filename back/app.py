from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
from .environment import KAFKA_BROKER, KAFKA_TOPIC, KAFKA_GROUP_ID
from .weather import fetch_location_key, fetch_current_weather
import json

app = Flask(__name__)

def fetch_weather_data(city_name):
    """Fetch weather data for a given city using AccuWeather API."""
    location_key = fetch_location_key(city_name)
    weather_info = fetch_current_weather(location_key)
    return weather_info

@app.route('/api/produce', methods=['GET'])
def produce_weather_data():
    city_name = request.args.get('city')
    weather_data = fetch_weather_data(city_name)
    
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    producer.send(KAFKA_TOPIC, weather_data)
    producer.flush()
    
    return jsonify({"message": f"Weather data for {city_name} has been sent to Kafka topic '{KAFKA_TOPIC}'."})

@app.route('/api/consume', methods=['GET'])
def consume_weather_data():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    weather_data = []
    for message in consumer:
        weather_data.append(message.value)
        if len(weather_data) >= 10:  # Limit the number of messages to fetch for simplicity
            break
    
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
