### Contributors
Ulysse Guillot, Léo Tran, Eliot Meurillon, Philippe Bonnafous
# Weather Kafka Application

This application demonstrates a simple producer-consumer system using Kafka, Flask, Nginx, and Cassandra to fetch and display weather data for a specified city.

## Overview

The application is divided into two main components:

- **Backend (`back/`)**: A Flask application that acts as both a producer and consumer of weather data. It fetches weather data from an external API, sends it to a Kafka topic as a producer, and also consumes messages from the same topic. Additionally, it interacts with Cassandra to store and retrieve weather data.
- **Frontend (`front/`)**: A simple web interface served by Nginx, allowing users to input a city name to fetch weather data and display it.

## Prerequisites

- Docker and Docker Compose
- An API key for the weather data provider (configured in `.env`)

## Configuration

The application requires a `.env` file at the root of the project for environment variables:

```env
WEATHER_API_KEY = "<Your_Weather_API_Key>"
KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "weather_data"
KAFKA_GROUP_ID = "weather_consumer_group"
CASSANDRA_HOST = "kafka-weather-app-cassandra-1"
CASSANDRA_PORT = 9042
CASSANDRA_KEYSPACE = "weather"
```

Replace `<Your_Weather_API_Key>` with your actual API key from the Accuweather API service.

## Running the Application

### Build and Run Containers

1. Use Docker Compose to build and run the application:

```bash
docker-compose up --build
```

2. Accessing the Frontend

Once the containers are up and running, the frontend can be accessed at http://localhost.

## Architecture

### Backend

* **Flask Application (back/app.py)**: Defines routes for producing and consuming weather data.
* **Kafka Producer & Consumer**: Uses kafka-python to interact with Kafka topics.
* **Weather Data Fetching (back/weather.py)**: Contains logic to fetch weather data from an external API.
* **Cassandra Integration (back/cassandra_util.py)**: Manages the connection to Cassandra and operations related to weather data storage and retrieval.

## Database Schema

The application uses a Cassandra database to store weather data. The schema is defined as follows:

### Frontend

* **Nginx (front/Dockerfile)**: Serves the static files and proxies API requests to the backend.
* **HTML & CSS (front/index.html, front/style.css)**: Defines the structure and style of the web interface.
* **JavaScript (front/app.js)**: Handles user interactions and API requests, including sending city names to the backend and displaying fetched weather data.

## Testing the Database Inside the Shell

To test inserting and querying data directly in the Cassandra database, follow these steps:

1. Ensure your Docker Compose services are running:
```bash
docker-compose up -d
```

2. Access the Cassandra container's shell:
```bash
docker exec -it kafka-weather-app-cassandra-1 bash
```

3. Start cqlsh to interact with Cassandra:
```bash
cqlsh
```

4. Insert data into the weather_data table. For example:
```bash
INSERT INTO weather.weather_data (city, temperature, description, epoch_time, has_precipitation) VALUES ('Test City', 22.5, 'Sunny', 123456789, false);
```

5. Query the data to verify the insertion:
```bash
SELECT * FROM weather.weather_data;
```