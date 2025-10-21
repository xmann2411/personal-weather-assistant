from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import PlanIn, PlanOut, Location, WeatherSummary, PlanPayload, Outfit, Activity, Alert
from services.weather import geocode, fetch_forecast, pick_slot, summarize
from services.ai import build_prompt, call_groq

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

@app.get("/health")
def health(): return {"ok": True}

@app.get("/weather")
async def get_weather(city: str, date: str):
    lat, lon, name, country = await geocode(city)
    fc = await fetch_forecast(lat, lon)
    slot = pick_slot(fc, date)
    if not slot:
        raise HTTPException(404, "Nema prognoze za taj datum (OWM 5-day limit).")
    summary = summarize(slot)
    return {
        "location": {"name": name, "country": country, "lat": lat, "lon": lon},
        "date": date,
        "weather": summary
    }

@app.post("/plan", response_model=PlanOut)
async def build_plan(req: PlanIn):
    lat, lon, name, country = await geocode(req.city)
    fc = await fetch_forecast(lat, lon)
    slot = pick_slot(fc, req.date)
    if not slot:
        raise HTTPException(404, "Nema prognoze za taj datum (OWM 5-day limit).")
    summary = summarize(slot)

    prompt = build_prompt(f"{name}, {country or ''}", req.date, summary, req.preferences or {})
    try:
        plan_json = await call_groq(prompt)
    except Exception:
        # jednostavan rule-based fallback
        alerts=[]
        if summary["pop"]>=50: alerts.append({"type":"rain","message":"Velika šansa kiše; ponesi kišobran i vodootpornu obuću."})
        if summary["wind"]>=8: alerts.append({"type":"wind","message":"Jak vjetar; izbjegni bicikl i planinarenje na izloženim mjestima."})
        outfit={"top":"majica dugih rukava","bottom":"traperice","outerwear":"lagana jakna","shoes":"udobne tenisice","accessories":["boca vode"]}
        plan_json={"outfit":outfit,"activities":[{"name":"šetnja kvartom","indoor":False,"timeSuggestion":"afternoon","note":"kratka lagana šetnja"}],
                   "alerts":alerts,"packing":["voda","punjač"],"rationale":"Rule-based fallback jer AI nije dostupan."}

    # mapiraj u pydantic modele
    weather = WeatherSummary(**summary)
    location = Location(name=name, country=country, lat=lat, lon=lon)
    outfit = Outfit(**plan_json["outfit"])
    activities = [Activity(**a) for a in plan_json["activities"]]
    alerts = [Alert(**a) for a in plan_json["alerts"]]
    plan = PlanPayload(outfit=outfit, activities=activities, alerts=alerts,
                       packing=plan_json["packing"], rationale=plan_json["rationale"])
    return PlanOut(location=location, date=req.date, weather=weather, plan=plan)
