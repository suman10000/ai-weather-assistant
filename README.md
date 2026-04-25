🌤️ AI Weather & Lifestyle Orchestration PipelineA modular, intelligent data pipeline that ingests real-time meteorological data, performs coordinate-based geocoding, executes WMO-standard data normalization, and leverages Generative AI (LLMs) to transform raw weather metrics into high-fidelity lifestyle and safety insights via a session-aware Streamlit dashboard.📌 Table of Contents🚀 Project Overview🏗 System Architecture🧠 Key Features📊 Tech Stack📁 Project Structure⚙ Data Pipeline Flow📈 Intelligence Capabilities🔐 Security & Configuration▶ How to Run Locally📚 Technical Demonstrations👨‍💻 Author🚀 Project OverviewThis project implements a real-world Decision-Support System designed to:Bridge the gap between raw environmental data and human actionability.Orchestrate a multi-stage API chain (Geocoding $\rightarrow$ Weather $\rightarrow$ LLM).Normalize technical WMO (World Meteorological Organization) codes into user-friendly conditions.Mitigate "information overload" through a Progressive Disclosure UI pattern.Demonstrate State Management in a stateless web environment.Ground Generative AI responses in "Real-Time Truth" to prevent model hallucinations.🏗 System ArchitecturePlaintextUser Query (City Name)
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
🧠 Key Features✔ Multi-Stage API Chaining: Seamlessly connects geospacial data with meteorological forecasts.✔ WMO Code Interpretation: Expert-level mapping of 90+ meteorological status codes to human descriptions.✔ Contextual Session Memory: Tracks user search history for comparative analytical queries.✔ Progressive Disclosure UI: Optimized UX that provides essential metrics first and detailed AI insights on-demand.✔ Grounding & Fact-Checking: AI prompts are dynamically injected with real-time data to ensure 100% factual accuracy.✔ Error Resiliency: Robust handling of API rate limits (429) and invalid location queries (404).📊 Tech StackLayerTechnologyFrontendStreamlit (Web UI Framework)OrchestrationPython 3.x, RequestsAI BrainGoogle Gemini 1.5 Flash (LLM)Data SourceOpen-Meteo REST APIsSDKGoogle GenAI Unified SDKState MgmtStreamlit Session State📁 Project StructurePlaintextAI-Weather-Lifestyle-Assistant/
│
├── app.py                 # Main Streamlit Web Application
├── weather_bot.py         # CLI/Terminal version of the assistant
│
├── requirements.txt       # Project dependencies
├── .gitignore             # Git exclusion rules
│
├── images/                # Screenshots & Architecture diagrams
│   └── architecture.png
│
└── README.md              # Project documentation
⚙ Data Pipeline Flow🔄 Ingestion & TransformationExtraction: Retrieves semi-structured JSON data from RESTful endpoints.Cleaning: Extracts relevant slices (Current vs Daily) and normalizes timestamps.Translation: Converts integers (WMO codes) into descriptive strings (e.g., 95 $\rightarrow$ Thunderstorm).🧠 Reasoning Layer (LLM)Prompt Engineering: Uses structured delimiters to enforce a 2-line response format.Actionable Logic: The model correlates temperature and precipitation to generate specific clothing and travel safety advice.📈 Intelligence CapabilitiesThe "Lifestyle Engine" provides targeted advice across four critical domains:👕 Clothing: Material and layering suggestions based on wind chill and humidity.⚠️ Safety: Proactive alerts regarding road conditions and visibility.🍲 Food/Drink: Contextual dietary suggestions (warming vs. cooling foods).🚶 Activity: Decision-support for travel vs. remote work based on precipitation probability.🔐 Security & ConfigurationImplemented using professional environment management:Credential Masking: API keys are managed via st.secrets and os.getenv.Stateless Persistence: Secure handling of history data within the client-side session.▶ How to Run Locally1️⃣ Clone and InstallBashgit clone https://github.com/yourusername/project-name.git
cd project-name
pip install -r requirements.txt
2️⃣ Configure API KeyAdd your key to your environment variables:Bash# For Terminal Version
export GEMINI_API_KEY="your_key_here"

# For Streamlit
# Create .streamlit/secrets.toml and add:
# GEMINI_API_KEY = "your_key_here"
3️⃣ LaunchBashstreamlit run app.py
📚 Technical DemonstrationsThis project showcases:✅ Full-Stack AI Integration: End-to-end development from API to UI.✅ Advanced Prompt Engineering: Controlling LLM output for specific UI constraints.✅ REST API Mastery: Handling multiple asynchronous data sources.✅ Product Thinking: Building for the user's "Action" rather than just showing "Data."👨‍💻 Author[Your Name] AI Developer & Data Enthusiast ---
