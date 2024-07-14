from cassandra_util import get_cassandra_session
from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from environment import KAFKA_BROKER, KAFKA_TOPIC, KAFKA_GROUP_ID
from weather import fetch_weather_data
import json

app = Flask(__name__)

@app.route('/produce', methods=['GET'])
def produce_weather_data():
    city_name = request.args.get('city')
    weather_data = fetch_weather_data(city_name)

    if not weather_data:
        return jsonify({"error": "Failed to fetch weather data for city."}), 400
    
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(KAFKA_TOPIC, weather_data)
    producer.close()

    session = get_cassandra_session()
    query = """
        INSERT INTO weather_data (city, temperature, description, epoch_time, has_precipitation)
        VALUES (%s, %s, %s, %s, %s)
        """
    city = weather_data.get('city', None).capitalize()
    temperature = weather_data.get('Temperature', {}).get('Metric', {}).get('Value', None)
    description = weather_data.get('WeatherText', None)
    epoch_time = weather_data.get('EpochTime', None)
    has_precipitation = weather_data.get('HasPrecipitation', None)

    if city is None or temperature is None or description is None or epoch_time is None or has_precipitation is None:
        return jsonify({"error": "Incomplete weather data."}), 400
    
    try:
        session.execute(query, (city, temperature, description, epoch_time, has_precipitation))
    except Exception as e:
        return jsonify({"error": f"Failed to store data in Cassandra: {str(e)}"}), 500

    return jsonify({"message": f"Weather data for {city_name} has been sent to Kafka topic '{KAFKA_TOPIC}' and stored in Cassandra."})

@app.route('/consume', methods=['GET'])
def consume_weather_data():
    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=KAFKA_BROKER,
                             group_id=KAFKA_GROUP_ID,
                             auto_offset_reset='earliest',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                             consumer_timeout_ms=5000)
    weather_data = []
    try:
        for message in consumer:
            weather_data.append(message.value)
            if len(weather_data) >= 10:
                break
    except KafkaError as e:
        return jsonify({"error": f"Failed to consume messages: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    finally:
        consumer.close()
    
    if not weather_data:
        return jsonify({"error": "No weather data found"}), 404

    return jsonify(weather_data)

@app.route('/weather/<city>', methods=['GET'])
def get_weather_data(city):
    session = get_cassandra_session()
    query = "SELECT * FROM weather_data WHERE city = %s"
    rows = session.execute(query, (city,))
    data = []
    for row in rows:
        data.append({"city": row.city, "temperature": row.temperature, "description": row.description, "epoch_time": row.epoch_time, "has_precipitation": row.has_precipitation})
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "No weather data found for the specified city"}), 404

#TO DO  
@app.route('/delete_weather/<city>', methods=['DELETE'])
def delete_weather_data(city):
    session = get_cassandra_session()
    query = "DELETE FROM weather_data WHERE city = %s"
    session.execute(query, (city,))
    return jsonify({"message": f"Weather data for {city} has been deleted."})

#Function to fetch data from Cassandra
def fetch_data_from_cassandra(city_name):
    session = get_cassandra_session()
    query = "SELECT * FROM weather_data WHERE city = %s"
    rows = session.execute(query, (city_name,))
    for row in rows:
        print(row.city, row.temperature, row.description, row.epoch_time, row.has_precipitation)

@app.route('/weather_data/<city>', methods=['GET'])
def get_weather_data_from_cassandra(city):
    # Assuming fetch_data_from_cassandra returns a dictionary or similar structure
    weather_data = fetch_data_from_cassandra(city)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Data not found"}), 404
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)