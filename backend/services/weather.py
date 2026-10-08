import logging
from datetime import date, datetime, timezone
from typing import Optional

import httpx
from fastapi import HTTPException

from config import OWM_KEY

log = logging.getLogger(__name__)

OWM_BASE = "https://api.openweathermap.org"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


async def _owm_get(path: str, params: dict, timeout: float) -> dict | list:
    if not OWM_KEY:
        raise HTTPException(500, "OWM_KEY nije postavljen u backend/.env.")
    try:
        async with httpx.AsyncClient(timeout=timeout) as c:
            r = await c.get(f"{OWM_BASE}{path}", params={**params, "appid": OWM_KEY})
    except httpx.RequestError as e:
        log.warning("OWM request failed: %s", e)
        raise HTTPException(503, "Vremenski servis trenutno nije dostupan. Pokušaj ponovno.")
    if r.status_code == 401:
        # novi OWM ključevi znaju biti neaktivni i do par sati nakon registracije
        raise HTTPException(502, "OpenWeatherMap je odbio API ključ (provjeri OWM_KEY ili pričekaj aktivaciju).")
    if r.status_code == 429:
        raise HTTPException(503, "Prekoračen je limit upita prema OpenWeatherMapu. Pokušaj za minutu.")
    if r.is_error:
        log.warning("OWM error %s: %s", r.status_code, r.text[:200])
        raise HTTPException(502, f"Greška vremenskog servisa ({r.status_code}).")
    return r.json()


async def geocode(city: str):
    data = await _owm_get("/geo/1.0/direct", {"q": city, "limit": 1}, timeout=10)
    if not data:
        raise HTTPException(404, f"Grad „{city}” nije pronađen.")
    x = data[0]
    return x["lat"], x["lon"], x.get("local_names", {}).get("hr") or x["name"], x.get("country")


async def fetch_forecast(lat: float, lon: float):
    return await _owm_get(
        "/data/2.5/forecast",
        {"lat": lat, "lon": lon, "units": "metric", "lang": "hr"},
        timeout=15,
    )


async def fetch_uv(lat: float, lon: float, day: date) -> Optional[float]:
    """Dnevni maksimalni UV indeks s Open-Meteo (besplatno, bez ključa).

    OWM 5-day forecast ne vraća UV, pa je ovo best-effort: ako ne uspije, vraća None.
    """
    params = {
        "latitude": lat, "longitude": lon, "daily": "uv_index_max",
        "timezone": "auto", "start_date": day.isoformat(), "end_date": day.isoformat(),
    }
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get(OPEN_METEO_URL, params=params)
            r.raise_for_status()
            value = r.json()["daily"]["uv_index_max"][0]
            return round(float(value), 1) if value is not None else None
    except Exception as e:
        log.info("UV fetch failed (%s), continuing without UV", e)
        return None


def _local_time(slot: dict, tz_offset: int) -> datetime:
    # OWM vraća dt u UTC; city.timezone je pomak u sekundama za lokalno vrijeme grada
    return datetime.fromtimestamp(slot["dt"] + tz_offset, tz=timezone.utc)


def available_dates(forecast_json: dict) -> list[date]:
    tz = forecast_json.get("city", {}).get("timezone", 0)
    return sorted({_local_time(s, tz).date() for s in forecast_json["list"]})


def pick_day(forecast_json: dict, day: date) -> list[dict]:
    """Svi 3-satni slotovi koji (po lokalnom vremenu grada) padaju na zadani dan."""
    tz = forecast_json.get("city", {}).get("timezone", 0)
    return [s for s in forecast_json["list"] if _local_time(s, tz).date() == day]


def summarize_day(slots: list[dict], tz_offset: int = 0) -> dict:
    """Sažetak cijelog dana iz 3-satnih slotova.

    Min/max/vjetar/kiša gledaju se preko cijelog dana; opis, ikona i
    subjektivni osjećaj uzimaju se iz slota najbližeg 13 h po lokalnom vremenu.
    """
    midday = min(slots, key=lambda s: abs(_local_time(s, tz_offset).hour - 13))
    wx = midday["weather"][0]
    humidity = [s["main"]["humidity"] for s in slots]
    return dict(
        min=round(min(s["main"]["temp_min"] for s in slots), 1),
        max=round(max(s["main"]["temp_max"] for s in slots), 1),
        feels=round(midday["main"]["feels_like"], 1),
        wind=round(max(s["wind"]["speed"] for s in slots), 1),
        pop=int(round(max(s.get("pop", 0) for s in slots) * 100)),
        uv=None,
        humidity=int(round(sum(humidity) / len(humidity))),
        desc=wx.get("description", ""),
        icon=wx.get("icon"),
    )
