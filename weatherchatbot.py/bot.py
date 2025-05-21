# app.py
from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

API_KEY = "2dadf5d99cb8d68c23b6bae93e4f1166"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather_desc = data['weather'][0]['description']
        temp = main['temp']
        humidity = main['humidity']
        wind_speed = data['wind']['speed']

        return (
            f"Weather in {city.title()}:\n"
            f"- Condition: {weather_desc.capitalize()}\n"
            f"- Temperature: {temp}°C\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind Speed: {wind_speed} m/s"
        )
    else:
        return "Sorry, I couldn't find weather information for that location."

def extract_city(user_input):
    match = re.search(r'in ([a-zA-Z\s]+)', user_input.lower())
    if match:
        city = match.group(1).strip()
        return city
    else:
        return None

def chatbot_response(user_input):
    user_input = user_input.lower()

    if any(greet in user_input for greet in ['hello', 'hi', 'hey']):
        return "Hello! Ask me about the weather in any city. For example, 'weather in London'."

    if any(word in user_input for word in ['weather', 'temperature', 'rain', 'sunny', 'cloudy', 'wind']):
        city = extract_city(user_input)
        if city:
            return get_weather(city)
        else:
            return "Please specify the city, for example: 'weather in London'."

    if any(bye in user_input for bye in ["bye", "exit", "quit"]):
        return "Goodbye! Stay safe and enjoy the weather."

    return "I can help with weather info. Try asking: 'weather in London' or 'temperature in New York'."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    bot_response = chatbot_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
