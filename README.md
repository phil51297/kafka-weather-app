# Weather Kafka Application

This application demonstrates a simple producer-consumer system using Kafka, Flask, and Nginx to fetch and display weather data for a specified city.

## Overview

The application is divided into two main components:

- **Backend (`back/`)**: A Flask application that acts as both a producer and consumer of weather data. It fetches weather data from an external API and sends it to a Kafka topic as a producer. It also consumes messages from the same topic.
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
```

Replace `<Your_Weather_API_Key>` with your actual API key for the weather service.

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

### Frontend

* **Nginx (front/Dockerfile)**: Serves the static files and proxies API requests to the backend.
* **HTML & CSS (front/index.html, front/style.css)**: Defines the structure and style of the web interface.
* **JavaScript (front/app.js)**: Handles user interactions and API requests.