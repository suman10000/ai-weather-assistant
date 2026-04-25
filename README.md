# 🌤️ AI Weather & Lifestyle Orchestration Pipeline

> A modular, intelligent data pipeline that ingests real-time meteorological data, performs coordinate-based geocoding, executes WMO-standard data normalization, and leverages Generative AI (LLMs) to transform raw weather metrics into high-fidelity lifestyle and safety insights via a session-aware Streamlit dashboard.

---

## 📌 Table of Contents

- [🚀 Project Overview](#-project-overview)
- [🏗 System Architecture](#-system-architecture)
- [🧠 Key Features](#-key-features)
- [📊 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙ Data Pipeline Flow](#-data-pipeline-flow)
- [📈 Intelligence Capabilities](#-intelligence-capabilities)
- [🔐 Security & Configuration](#-security--configuration)
- [▶ How to Run Locally](#-how-to-run-locally)
- [📚 Technical Demonstrations](#-technical-demonstrations)
- [👨‍💻 Author](#-author)

---

## 🚀 Project Overview

This project implements a real-world **Decision-Support System** designed to:

- Bridge the gap between **raw environmental data** and **human actionability**.
- Orchestrate a multi-stage API chain (Geocoding → Weather → LLM).
- Normalize technical WMO (World Meteorological Organization) codes into user-friendly conditions.
- Mitigate "information overload" through a **Progressive Disclosure** UI pattern.
- Demonstrate **State Management** in a stateless web environment.
- Ground Generative AI responses in "Real-Time Truth" to prevent model hallucinations.

---

## 🏗 System Architecture



```text
User Query (City Name)
            ↓
Stage 1: Geocoding Engine (Open-Meteo Search)
            ↓
Latitude / Longitude / Full Location Metadata
            ↓
Stage 2: Weather Ingestion (Open-Meteo Forecast API)
            ↓
Raw JSON Response (WMO Codes, Temp, Wind, Rain %)
            ↓
Stage 3: Data Normalization (Mapping Layer)
            ↓
Structured Context Object (Human-Readable Metrics)
            ↓
Stage 4: LLM Reasoning (Google Gemini 1.5 Flash)
            ↓
Session-Aware Interactive Dashboard (Streamlit)


🧠 Key Features✔ Multi-Stage API Chaining: Seamlessly connects geospatial data with meteorological forecasts.✔ WMO Code Interpretation: Expert-level mapping of 90+ meteorological status codes to human descriptions and emojis.✔ Contextual Session Memory: Tracks user search history for comparative analytical queries using Streamlit Session State.✔ Progressive Disclosure UI: Optimized UX that provides essential metrics first and detailed AI insights on-demand.✔ Grounding & Fact-Checking: AI prompts are dynamically injected with real-time data to ensure 100% factual accuracy in recommendations.✔ Error Resiliency: Robust handling of API rate limits (429), resource exhaustion, and invalid location queries.
📊 Tech Stack
LayerTechnology
FrontendStreamlit (Web UI Framework)OrchestrationPython 3.x, RequestsAI BrainGoogle Gemini 1.5 Flash (LLM)Data SourceOpen-Meteo REST APIsSDKGoogle GenAI Unified SDKState MgmtStreamlit Session State📁 Project StructurePlaintextAI-Weather-Lifestyle-Assistant/
│
├── app.py                 # Main Streamlit Web Application
├── weather_bot.py         # CLI/Terminal version of the assistant
│
├── requirements.txt       # Project dependencies
├── .gitignore             # Git exclusion rules
│
└── README.md              # Project documentation
⚙ Data Pipeline Flow🔄 Ingestion & TransformationExtraction: Retrieves semi-structured JSON data from RESTful endpoints (Open-Meteo).Cleaning: Extracts relevant slices (Current Conditions vs Daily Forecast) and normalizes timestamps for readability.Translation: Converts system-level integers (WMO codes) into descriptive strings (e.g., 95 → Thunderstorm).🧠 Reasoning Layer (LLM)Prompt Engineering: Uses structured delimiters to enforce a concise, 2-line response format per category.Actionable Logic: The model correlates temperature, wind speed, and precipitation probability to generate specific, data-backed advice.📈 Intelligence CapabilitiesThe "Lifestyle Engine" provides targeted advice across four critical domains:👕 Clothing: Material and layering suggestions based on temperature and wind chill.⚠️ Safety: Proactive alerts regarding road conditions, visibility, or wind hazards.🍲 Food/Drink: Contextual dietary suggestions (e.g., warming foods for cold snaps).🚶 Activity: Decision-support for travel vs. indoor activities based on rain probability.🔐 Security & ConfigurationImplemented using professional environment management:Credential Masking: API keys are managed via st.secrets (Production) and os.getenv (Development).Stateless Persistence: Secure handling of history data within the client-side session to maintain privacy.
▶ How to Run Locally1️⃣ Clone and InstallBashgit clone [https://github.com/yourusername/ai-weather-assistant.git](https://github.com/yourusername/ai-weather-assistant.git)
cd ai-weather-assistant
pip install -r requirements.txt
2️⃣ Configure API KeyAdd your key to your environment:For Streamlit: Create a .streamlit/secrets.toml file and add:Ini, TOMLGEMINI_API_KEY = "your_key_here"
For Terminal Version:Bashexport GEMINI_API_KEY="your_key_here"
3️⃣ LaunchBashstreamlit run app.py
📚 Technical Demonstrations
This project showcases:✅ Full-Stack AI Integration: End-to-end development from raw API ingestion to a polished UI.✅ Advanced Prompt Engineering: Controlling LLM output to adhere to strict UI and formatting constraints.✅ REST API Mastery: Handling multiple asynchronous data sources and complex JSON parsing.✅ Product Thinking: Designing a tool focused on user "Actionability" rather than just data visualization.
