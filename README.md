# Personal Weather Assistant ☀️🤖

Aplikacija koja kombinira **vremenske podatke (OpenWeatherMap)** i **AI analizu (Groq LLM)** te daje **personalizirane preporuke**: odjeća, aktivnosti, upozorenja i packing lista.

**Stack:**  
- Frontend: React + TypeScript (Create React App)  
- Backend: FastAPI (Python)  
- API: OpenWeatherMap (free tier)  
- LLM: Groq API (free tier)

---
## 🚀 Pokretanje (lokalno)

### 0) Preduvjeti
- Node.js LTS (npr. 18+)
- Python 3.10+ (radi i novije)
- OpenWeatherMap API ključ (free): https://home.openweathermap.org/api_keys  
- Groq API ključ (free): https://console.groq.com/keys

---

### 1) Backend (FastAPI)

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate        # PowerShell (Windows)
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

# Kreiraj .env (vidi primjer dolje), pa:
Kreiraj .env fajl u /backend direktoriju:

OPENWEATHER_API_KEY=5a9e79e557cb0265ae5d9221d8e9f103

Pokreni server:
python -m uvicorn app:app --reload --port 8000


Test:
http://localhost:8000/health → { "ok": true }
http://localhost:8000/docs (Swagger)

Napomena: OWM 5-day/3h forecast pokriva ~5 dana unaprijed. Za datume izvan raspona endpoint će vratiti poruku da nema prognoze.

### 2) Frontend (React + TS)
U drugom terminalu (root projekta):
npm install
npm start

Aplikacija je dostupna na:
http://localhost:3000

## Struktura projekta:
PERSONALWEATHERASSISTANT2/
├── backend/ # FastAPI backend (Python)
├── src/ # React frontend (TypeScript)
├── public/ # Statički fajlovi
├── package.json # Frontend konfiguracija
├── requirements.txt # Backend zavisnosti
└── README.md

## Primjeri korištenja API-ja
# Health check
curl http://localhost:8000/health

# Prognoza za određeni grad i datum
curl "http://localhost:8000/weather?city=Samobor&date=2025-10-21"
curl "http://localhost:8000/weather?city=Zagreb&date=2025-10-22"


Planirane funkcionalnosti (roadmap):
- Preporuke aktivnosti po vremenu
- AI analiza prognoze
- Offline cache (LocalStorage)

Autor:
Karla Axmann
karla@brrax.hr
