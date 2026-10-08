from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient

import app as app_module
from models import PlanPayload
from services.ai import AIUnavailable

DAY = date(2026, 10, 21)


def owm_slot(hour_utc: int, temp: float):
    dt = int(datetime(2026, 10, 21, hour_utc, tzinfo=timezone.utc).timestamp())
    return {"dt": dt, "main": {"temp_min": temp, "temp_max": temp, "feels_like": temp, "humidity": 70},
            "wind": {"speed": 3}, "pop": 0.2, "weather": [{"description": "oblačno", "icon": "04d"}]}


@pytest.fixture
def client(monkeypatch):
    async def geocode(city):
        return 45.81, 15.98, "Zagreb", "HR"

    async def fetch_forecast(lat, lon):
        return {"city": {"timezone": 7200}, "list": [owm_slot(8, 12), owm_slot(11, 17)]}

    async def fetch_uv(lat, lon, day):
        return 3.1

    monkeypatch.setattr(app_module, "geocode", geocode)
    monkeypatch.setattr(app_module, "fetch_forecast", fetch_forecast)
    monkeypatch.setattr(app_module, "fetch_uv", fetch_uv)
    return TestClient(app_module.app)


def test_plan_uses_ai_when_available(client, monkeypatch):
    plan = PlanPayload.model_validate({
        "outfit": {"top": "džemper", "bottom": "traperice", "outerwear": "jakna", "shoes": "tenisice"},
        "activities": [{"name": "Muzej Mimara", "indoor": True}],
    })

    async def generate_plan(messages):
        return plan

    monkeypatch.setattr(app_module, "generate_plan", generate_plan)
    r = client.post("/plan", json={"city": "Zagreb", "date": DAY.isoformat()})
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "ai"
    assert body["weather"]["min"] == 12 and body["weather"]["max"] == 17 and body["weather"]["uv"] == 3.1
    assert body["plan"]["activities"][0]["name"] == "Muzej Mimara"


def test_plan_falls_back_when_ai_fails(client, monkeypatch):
    async def generate_plan(messages):
        raise AIUnavailable("down")

    monkeypatch.setattr(app_module, "generate_plan", generate_plan)
    r = client.post("/plan", json={"city": "Zagreb", "date": DAY.isoformat()})
    assert r.status_code == 200
    assert r.json()["source"] == "fallback"


def test_plan_date_out_of_range_returns_404_with_available_range(client):
    r = client.post("/plan", json={"city": "Zagreb", "date": "2026-11-30"})
    assert r.status_code == 404
    assert "dostupna od 21.10." in r.json()["detail"]


def test_plan_rejects_invalid_input(client):
    assert client.post("/plan", json={"city": "", "date": "2026-10-21"}).status_code == 422
    assert client.post("/plan", json={"city": "Zagreb", "date": "21.10.2026"}).status_code == 422
