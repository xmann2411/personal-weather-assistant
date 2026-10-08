# Personal Weather Assistant ☀️🤖

An application that combines **weather data (OpenWeatherMap)** with **AI analysis (Groq LLM)** to provide **personalized recommendations** — clothing suggestions, outdoor activity ideas, weather alerts, and packing lists.

If the AI is unavailable (missing key, rate limit, invalid response), the backend falls back to a **rule-based plan** based on temperature, rain, wind and UV, so the app always returns useful advice.

---

## 🧩 Tech Stack

- **Frontend:** React + TypeScript (Create React App)
- **Backend:** FastAPI (Python)
- **Weather:** OpenWeatherMap 5-day / 3-hour forecast (free tier)
- **UV index:** Open-Meteo (free, no API key)
- **LLM:** Groq API (free tier)

---

## 🚀 Running Locally

### 0) Prerequisites

- Node.js LTS (v18+)
- Python 3.10+
- OpenWeatherMap API key (free): [https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)
  — new keys can take up to a couple of hours to activate
- Groq API key (free): [https://console.groq.com/keys](https://console.groq.com/keys)

### 1) Backend (FastAPI)

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate        # PowerShell (Windows)
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

Create `backend/.env` from the example and fill in your keys:

```bash
cp .env.example .env            # PowerShell: Copy-Item .env.example .env
```

```env
OWM_KEY=your_openweathermap_key
GROQ_API_KEY=your_groq_key
```

Optional settings (see `.env.example`): `GROQ_MODELS` (comma-separated, first one is primary, the rest are fallbacks) and `CORS_ORIGINS`.

Run the server:

```bash
python -m uvicorn app:app --reload --port 8000
```

- http://localhost:8000/health → `{ "ok": true }`
- http://localhost:8000/docs → Swagger UI

### 2) Frontend (React + TS)

In a second terminal, from the project root:

```bash
npm install
npm start
```

The app will be available at http://localhost:3000.
To point the frontend at a different backend, set `REACT_APP_API_URL` (e.g. in a `.env.local` file in the project root).

---

## 🧪 Tests

```bash
# backend
cd backend
pip install -r requirements-dev.txt
python -m pytest

# frontend (project root)
npm test
```

---

## 📡 API

| Method | Path       | Description |
|--------|------------|-------------|
| GET    | `/health`  | Health check |
| GET    | `/weather?city=Zagreb&date=YYYY-MM-DD` | Daily weather summary for a city |
| POST   | `/plan`    | Weather + personalized plan |

```bash
curl "http://localhost:8000/weather?city=Samobor&date=2026-10-21"

curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"city": "Zagreb", "date": "2026-10-21", "preferences": {"notes": "travelling with kids"}}'
```

The `/plan` response contains `source: "ai" | "fallback"` so the UI can show where the recommendations came from.

**How the daily summary is computed:** all 3-hour forecast slots that fall on the selected date *in the city's local time* are aggregated — min/max temperature over the whole day, the highest wind and rain probability, average humidity, and the description/icon from the slot closest to 13:00.

> The OWM free forecast covers roughly 5 days ahead. For dates outside that range the API returns `404` with the available date range.

---

## 🗂️ Project Structure

```
personal-weather-assistant/
├── backend/                  # FastAPI backend (Python)
│   ├── app.py                # API endpoints
│   ├── config.py             # env variables (.env)
│   ├── models.py             # Pydantic models
│   ├── services/
│   │   ├── weather.py        # OpenWeatherMap + Open-Meteo UV, daily summary
│   │   ├── ai.py             # Groq prompt & call
│   │   └── fallback.py       # rule-based plan when AI is unavailable
│   ├── tests/                # pytest
│   ├── requirements.txt
│   └── .env.example
├── src/                      # React frontend (TypeScript)
│   ├── components/           # UI cards and search form
│   ├── hooks/usePlan.ts
│   ├── services/             # API client
│   └── types/plan.ts
├── public/
└── package.json
```

---

## 🛣️ Roadmap

- Offline cache of the last plan (LocalStorage)
- Multi-day view (whole 5-day forecast at once)
- Migrate the frontend from Create React App to Vite
