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
    
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(KAFKA_TOPIC, weather_data)
    producer.close()
    
    return jsonify({"message": f"Weather data for {city_name} has been sent to Kafka topic '{KAFKA_TOPIC}'."})

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

if __name__ == '__main__':
    app.run(debug=True, port=5001)