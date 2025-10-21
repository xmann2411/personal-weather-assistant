import os, httpx
from fastapi import HTTPException
from dotenv import load_dotenv
load_dotenv()
OWM=os.getenv("OWM_KEY")

async def geocode(city: str):
    url=f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OWM}"
    async with httpx.AsyncClient(timeout=10) as c:
        r=await c.get(url); r.raise_for_status()
        data=r.json()
        if not data: raise HTTPException(404, "City not found")
        x=data[0]; return x["lat"], x["lon"], x["name"], x.get("country")

async def fetch_forecast(lat: float, lon: float):
    url=f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OWM}&units=metric&lang=hr"
    async with httpx.AsyncClient(timeout=15) as c:
        r=await c.get(url); r.raise_for_status()
        return r.json()

def pick_slot(forecast_json: dict, date_str: str):
    slots=[i for i in forecast_json["list"] if i["dt_txt"].startswith(date_str)]
    if not slots: return None
    for s in slots:
        if s["dt_txt"].endswith("12:00:00"): return s
    return slots[len(slots)//2]

def summarize(slot: dict):
    m=slot["main"]; w=slot["wind"]; wx=slot["weather"][0]
    pop=int(round(slot.get("pop",0)*100))
    uv = 5  # heuristika; OWM 5-day nema UV (dovoljno za preporuke)
    return dict(
        min=m.get("temp_min"), max=m.get("temp_max"), feels=m.get("feels_like"),
        wind=w.get("speed"), pop=pop, uv=uv, humidity=m.get("humidity"),
        desc=wx.get("description"), icon=wx.get("icon")
    )
