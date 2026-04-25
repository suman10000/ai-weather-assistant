import streamlit as st
import requests
from google import genai
from google.api_core import exceptions


st.set_page_config(page_title="AI Weather Assistant", page_icon="🌤️",layout="wide")


GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-flash-latest"


if "history" not in st.session_state:
    st.session_state.history = []




def get_coordinates(city_name):
    """Geocoding API"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    try:
        res = requests.get(url).json()
        if "results" in res:
            result = res["results"][0]
            return result["latitude"], result["longitude"], f"{result['name']}, {result['country']}"
    except: return None
    return None

def get_weather(lat, lon):
    """Stage 2: Enhanced Weather API with WMO Mapping"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto"
    
    
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
            day_cond = wmo_codes.get(daily['weather_code'][i], "Cloudy").split(" ")[1] # Just the text
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

def get_ai_response(prompt):
    """Stage 3: Gemini AI Generation"""
    try:
        response = client.models.generate_content(model=MODEL_ID, contents=prompt)
        return response.text
    except exceptions.ResourceExhausted:
        return "⚠️ Quota reached. Please wait 60 seconds."
    except Exception as e:
        return f"AI Error: {e}"

# Streamlit UI

st.title("🤖 AI Weather & Lifestyle Assistant")
st.markdown("Providing data-driven insights for your daily planning.")

city_input = st.text_input("Search for a city:", placeholder="e.g. Mumbai, Tokyo, Paris")

if city_input:
    location = get_coordinates(city_input)
    
    if location:
        lat, lon, full_name = location
        weather = get_weather(lat, lon)
        
        if weather:
            st.write(f"## 📍 {full_name}")
            st.caption(f"Data synchronized at: {weather['time']}")

            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Current Condition", weather['condition'])
            m2.metric("Temperature", f"{weather['temp']}°C")
            m3.metric("Rain Chance", f"{weather['rain_chance']}%")
            m4.metric("Wind Speed", f"{weather['wind']} km/h")

            
            summary_prompt = f"In one friendly sentence, greet the user and describe the {weather['condition']} in {full_name} today."
            with st.spinner("AI is greeting you..."):
                summary = get_ai_response(summary_prompt)
                st.info(f"✨ {summary}")

            
            st.write("### 📅 3-Day Forecast")
            f_col1, f_col2, f_col3 = st.columns(3)
            forecast_lines = weather['forecast'].split('\n')
            cols = [f_col1, f_col2, f_col3]
            for i in range(3):
                with cols[i]:
                    st.success(forecast_lines[i].replace(": ", "\n"))

            
            st.divider()
            st.write("### 💡 AI Lifestyle Insights")
            if st.button("Generate Detailed Advice"):
                with st.spinner("Analyzing patterns for personalized advice..."):
                    history_context = "\n".join(st.session_state.history[-4:])
                    advice_prompt = f"""
                    You are a lifestyle assistant. Use this data for {full_name}:
                    Current: {weather['temp']}°C, {weather['condition']}, {weather['rain_chance']}% rain.
                    Forecast: {weather['forecast']}
                    
                    Provide exactly 2 lines of advice for each:
                    👕 Clothing: (Instruction + Reason)
                    ⚠️ Safety: (Instruction + Reason)
                    🍲 Food/Drink: (Instruction + Reason)
                    🚶 Travel/Activity: (Instruction + Reason)
                    
                    Keep it professional and helpful.
                    """
                    advice = get_ai_response(advice_prompt)
                    
                    
                    st.session_state.history.append(f"Checked: {full_name}")
                    st.session_state.history.append(f"AI Advice: {advice[:50]}...")
                    
                    st.markdown(advice)
    else:
        st.error("City not found. Please try another location.")


with st.sidebar:
    st.header("Search History")
    if st.session_state.history:
        for msg in st.session_state.history:
            st.write(f"- {msg}")
        if st.button("Clear Memory"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("No recent activity.")
    
    st.divider()
    st.subheader("How to use")
    st.write("1. Enter a city name.\n2. View real-time metrics.\n3. Click 'Generate' for AI tips.")