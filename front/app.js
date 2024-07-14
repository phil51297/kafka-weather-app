htmx.on("#weatherData", "htmx:afterSettle", function (event) {
  try {
    const data = JSON.parse(event.detail.xhr.response);
    const weatherDataDiv = document.getElementById("weatherData");
    weatherDataDiv.innerHTML = "";
    data.forEach((weather) => {
      const weatherDiv = document.createElement("div");
      weatherDiv.innerText = JSON.stringify(weather, null, 2);
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
