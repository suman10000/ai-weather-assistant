import os
import requests
import time
from google import genai
from google.api_core import exceptions  


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-flash-latest"

def get_brief_summary(city, temp, wind):
    """Generates a single, friendly sentence about the current weather."""
    prompt = f"Summarize the weather in {city} ({temp}°C, {wind} km/h) in exactly one friendly, creative sentence."
    try:
        response = client.models.generate_content(model=MODEL_ID, contents=prompt)
        return response.text.strip()
    except Exception:
        return f"It's currently {temp}°C in {city} with winds at {wind} km/h."

def get_concise_advice(city, weather_info):
    """Generates a balanced 2-line advice per category."""
    prompt = f"""
    Based on {city}'s weather ({weather_info['temp']}°C, {weather_info['wind']}km/h) and 3-day forecast, 
    provide exactly 2 lines of advice for each category below.
    
    Format each category as:
    Category Name:
    - Line 1: Clear, actionable instruction.
    - Line 2: A short reason or tip based on the data.

    Categories: 👕 Clothing, ⚠️ Safety, 🍲 Food, 🚶 Travel/Activity
    """
    try:
        response = client.models.generate_content(model=MODEL_ID, contents=prompt)
        return response.text
    except exceptions.ResourceExhausted:
        return "⚠️ Quota reached. Let's try again in a minute!"
    except Exception as e:
        return f"Advice Error: {e}"

def get_coordinates(city_name):
    """Stage 1: Convert city name to coordinates."""
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    try:
        response = requests.get(geo_url)
        response.raise_for_status()
        data = response.json()
        if "results" in data:
            res = data["results"][0]
            return res["latitude"], res["longitude"], f"{res['name']}, {res['country']}"
        return None
    except Exception: return None

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto"
    
    # WMO Weather Interpretation Codes
    wmo_codes = {
        0: "☀️ Clear Sky", 1: "🌤️ Mainly Clear", 2: "⛅ Partly Cloudy", 3: "☁️ Overcast",
        45: "🌫️ Foggy", 51: "🌦️ Light Drizzle", 61: "🌧️ Slight Rain", 80: "⛈️ Rain Showers",
        95: "🌩️ Thunderstorm"
    }

    try:
        data = requests.get(url).json()
        current = data.get("current_weather", {})
        daily = data.get("daily", {})
        
        condition = wmo_codes.get(current.get("weathercode"), "🌈 Variable Conditions")
        rain_chance = daily.get("precipitation_probability_max", [0])[0]

        forecast_list = []
        for i in range(3):
            day_cond = wmo_codes.get(daily['weather_code'][i], "Cloudy")
            forecast_list.append(f"{daily['time'][i]}: {day_cond}, {daily['temperature_2m_max'][i]}°C/{daily['temperature_2m_min'][i]}°C")

        return {
            "temp": current.get("temperature"),
            "wind": current.get("windspeed"),
            "condition": condition,
            "rain_chance": rain_chance,
            "time": current.get("time").replace("T", " "),
            "forecast": "\n".join(forecast_list)
        }
    except: return None

def main():
    print("--- This is your Smart Weather Assistant ---")
    
    while True:
        city_input = input("\nEnter city name (or 'exit'): ").strip()
        if city_input.lower() == 'exit': break

        
        location = get_coordinates(city_input)
        if not location:
            print("City not found."); continue
        
        lat, lon, full_name = location
        weather_info = get_weather(lat, lon)
        
        
        print(f"\n📍 Location: {full_name}")
        print(f"🌡️  Current: {weather_info['temp']}°C | 💨 Wind: {weather_info['wind']} km/h")
        
        brief_summary = get_brief_summary(full_name, weather_info['temp'], weather_info['wind'])
        print(f"\n✨ {brief_summary}")

        
        choice = input("\nWould you like lifestyle & travel advice for this weather? (y/n): ").lower()
        
        if choice == 'y':
            print("Fetching advice... 🧠")
            advice = get_concise_advice(full_name, weather_info)
            print("\n" + "-"*30)
            print(advice)
            print("-"*30)
        else:
            print("No problem! Let me know if you need anything else.")

if __name__ == "__main__":
    main()

