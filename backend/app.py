import asyncio
import logging
from datetime import date

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS
from models import PlanIn, PlanOut, Location, WeatherSummary
from services.weather import geocode, fetch_forecast, fetch_uv, pick_day, available_dates, summarize_day
from services.ai import AIUnavailable, build_messages, generate_plan
from services.fallback import rule_based_plan

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("app")

app = FastAPI(title="Personal Weather Assistant API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS, allow_methods=["GET", "POST"], allow_headers=["*"],
)


async def load_weather(city: str, day: date) -> tuple[Location, dict]:
    lat, lon, name, country = await geocode(city)
    fc, uv = await asyncio.gather(fetch_forecast(lat, lon), fetch_uv(lat, lon, day))

    slots = pick_day(fc, day)
    if not slots:
        days = available_dates(fc)
        raise HTTPException(
            404,
            f"Nema prognoze za {day.strftime('%d.%m.%Y.')} Prognoza je dostupna "
            f"od {days[0].strftime('%d.%m.')} do {days[-1].strftime('%d.%m.%Y.')}",
        )

    summary = summarize_day(slots, fc.get("city", {}).get("timezone", 0))
    summary["uv"] = uv
    return Location(name=name, country=country, lat=lat, lon=lon), summary


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/weather")
async def get_weather(city: str = Query(min_length=1, max_length=100), date: date = Query()):
    location, summary = await load_weather(city.strip(), date)
    return {"location": location, "date": date, "weather": WeatherSummary(**summary)}


@app.post("/plan", response_model=PlanOut)
async def build_plan(req: PlanIn):
    location, summary = await load_weather(req.city.strip(), req.date)
    place = f"{location.name}, {location.country}" if location.country else location.name

    try:
        plan = await generate_plan(build_messages(place, req.date.isoformat(), summary, req.preferences))
        source = "ai"
    except AIUnavailable as e:
        log.warning("Using rule-based fallback: %s", e)
        plan = rule_based_plan(summary)
        source = "fallback"

    return PlanOut(location=location, date=req.date, weather=WeatherSummary(**summary), plan=plan, source=source)
