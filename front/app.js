htmx.on("#weatherData", "htmx:afterSettle", function (event) {
  try {
    const data = JSON.parse(event.detail.xhr.response);
    const weatherDataDiv = document.getElementById("weatherData");
    weatherDataDiv.innerHTML = "";
    data.forEach((weather) => {
      const weatherDiv = document.createElement("div");

      const city = document.createElement("h3");
      city.innerText = weather.city;
      weatherDiv.appendChild(city);

      const temperature = document.createElement("p");
      temperature.innerText = `Temperature: ${weather.temperature} °C`;
      weatherDiv.appendChild(temperature);

      const description = document.createElement("p");
      description.innerText = `Description: ${weather.description}`;
      weatherDiv.appendChild(description);

      const epochTime = document.createElement("p");
      epochTime.innerText = `Epoch Time: ${weather.epoch_time}`;
      weatherDiv.appendChild(epochTime);

      const hasPrecipitation = document.createElement("p");
      hasPrecipitation.innerText = `Has Precipitation: ${weather.has_precipitation}`;
      weatherDiv.appendChild(hasPrecipitation);
    });
  } catch (error) {
    console.error("Error parsing weather data:", error);
  }
});

htmx.on("#producerMessage", "htmx:afterSettle", function (event) {
  try {
    const data = JSON.parse(event.detail.xhr.response);
    document.getElementById("producerMessage").innerText =
      data.message || "Weather data successfully sent!";
  } catch (error) {
    console.error("Error parsing producer response:", error);
  }
});
