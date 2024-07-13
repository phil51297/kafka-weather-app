const sendWeatherData = () => {
    const cityName = document.getElementById('cityInput').value;
    fetch(`/api/produce?city=${cityName}`)
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            document.getElementById('producerMessage').innerText = "Weather data successfully sent!";
        })
        .catch(error => console.error('Error:', error));
};

const fetchWeatherData = () => {
    fetch('/api/consume')
        .then(response => response.json())
        .then(data => {
            const weatherDataDiv = document.getElementById('weatherData');
            weatherDataDiv.innerHTML = '';
            data.forEach(weather => {
                const weatherDiv = document.createElement('div');
                weatherDiv.innerText = JSON.stringify(weather);
                weatherDataDiv.appendChild(weatherDiv);
            });
        })
        .catch(error => console.error('Error:', error));
};

document.getElementById("produceForm").onsubmit = async (event) => {
  event.preventDefault();
  const city = document.getElementById("city").value;
  const response = await fetch(`http://backend:5001/api/produce?city=${city}`);
  const data = await response.json();
  document.getElementById("produceResult").innerText = JSON.stringify(data, null, 2);
};

document.getElementById("consumeButton").onclick = async () => {
  const response = await fetch('http://backend:5001/api/consume');
  const data = await response.json();
  document.getElementById("consumeResult").innerText = JSON.stringify(data, null, 2);
};
