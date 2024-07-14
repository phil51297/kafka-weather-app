CREATE KEYSPACE IF NOT EXISTS weather WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE weather;
CREATE TABLE IF NOT EXISTS weather_data (
  city text PRIMARY KEY,
  temperature double, 
  description text,
  epoch_time bigint,
  has_precipitation boolean
);