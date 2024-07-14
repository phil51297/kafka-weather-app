htmx.on("#weatherData", "htmx:afterSettle", function (event) {
  try {
    const data = JSON.parse(event.detail.xhr.response);
    const weatherDataDiv = document.getElementById("weatherData");
    weatherDataDiv.innerHTML = "";
    data.forEach((weather) => {
      const weatherDiv = document.createElement("div");
      weatherDiv.innerHTML = `
        <p><strong>City:</strong> ${weather.city}</p>
        <p><strong>Temperature:</strong> ${weather.Temperature.Metric.Value}°${
        weather.Temperature.Metric.Unit
      }</p>
        <p><strong>Description:</strong> ${weather.WeatherText}</p>
        <p><strong>Time:</strong> ${new Date(
          weather.EpochTime * 1000
        ).toLocaleString()}</p>
        <p><strong>Precipitation:</strong> ${
          weather.HasPrecipitation ? "Yes" : "No"
        }</p>
        <p><strong>Day Time:</strong> ${weather.IsDayTime ? "Yes" : "No"}</p>
      `;
      weatherDataDiv.appendChild(weatherDiv);
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

htmx.on("#citySelect", "htmx:afterSettle", function (event) {
  try {
    const cities = JSON.parse(event.detail.xhr.response);
    const citySelect = document.getElementById("citySelect");
    citySelect.innerHTML = '<option value="">Select a city</option>';
    cities.forEach((city) => {
      const option = document.createElement("option");
      option.value = city;
      option.textContent = city;
      citySelect.appendChild(option);
    });
  } catch (error) {
    console.error("Error parsing cities data:", error);
  }
});

htmx.on("#weatherDataCassandra", "htmx:afterSettle", function (event) {
  try {
    const data = JSON.parse(event.detail.xhr.response);
    const weatherDataDiv = document.getElementById("weatherDataCassandra");
    weatherDataDiv.innerHTML = "";
    data.forEach((weather) => {
      const weatherDiv = document.createElement("div");
      weatherDiv.innerHTML = `
        <p><strong>City:</strong> ${weather.city}</p>
        <p><strong>Temperature:</strong> ${weather.temperature}°C</p>
        <p><strong>Description:</strong> ${weather.description}</p>
        <p><strong>Time:</strong> ${new Date(
          weather.epoch_time * 1000
        ).toLocaleString()}</p>
        <p><strong>Precipitation:</strong> ${
          weather.has_precipitation ? "Yes" : "No"
        }</p>
        <hr>
      `;
      weatherDataDiv.appendChild(weatherDiv);
    });
  } catch (error) {
    console.error("Error parsing weather data:", error);
  }
});
