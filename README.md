# Personal Weather Assistant ☀️🤖

An application that combines **weather data (OpenWeatherMap)** with **AI analysis (Groq LLM)** to provide **personalized recommendations** — clothing suggestions, outdoor activity ideas, weather alerts, and packing lists.

---

## 🧩 Tech Stack

- **Frontend:** React + TypeScript (Create React App)  
- **Backend:** FastAPI (Python)  
- **API:** OpenWeatherMap (free tier)  
- **LLM:** Groq API (free tier)

---

## 🚀 Running Locally

### 0) Prerequisites

- Node.js LTS (v18+)
- Python 3.10+ (newer versions also work)
- OpenWeatherMap API key (free): [https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)  
- Groq API key (free): [https://console.groq.com/keys](https://console.groq.com/keys)

---

### 1) Backend (FastAPI)

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate        # PowerShell (Windows)
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt


# Run the server:
python -m uvicorn app:app --reload --port 8000


Test endpoints:
http://localhost:8000/health → { "ok": true }
http://localhost:8000/docs (Swagger)

Note: The OWM “5-day/3-hour forecast” API provides data for about 5 days ahead.
For dates outside this range, the endpoint will return a message saying no forecast is available.

---

### 2) Frontend (React + TS)
Open a second terminal (from the project root):
npm install
npm start

The app will be available at:
http://localhost:3000

## Project Structure:
PERSONALWEATHERASSISTANT2/
├── backend/ # FastAPI backend (Python)
├── src/ # React frontend (TypeScript)
├── public/ # Static files
├── package.json # Frontend konfiguracija
├── requirements.txt # Backend zavisnosti
└── README.md

## API Usage Examples
# Health check
curl http://localhost:8000/health

# Weather forecast for a specific city and date
curl "http://localhost:8000/weather?city=Samobor&date=2025-10-21"
curl "http://localhost:8000/weather?city=Zagreb&date=2025-10-22"


## Planned Features (roadmap):
- Weather-based activity recommendations
- AI-powered forecast analysis
- Offline cache (LocalStorage)

## Author:
Karla Axmann
karla@brrax.hr
