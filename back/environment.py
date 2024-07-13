import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "kafka-weather-app-cassandra-1")
CASSANDRA_PORT = os.getenv("CASSANDRA_PORT", 9042)
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "weather")