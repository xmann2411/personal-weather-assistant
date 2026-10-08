from datetime import date, datetime, timezone

from services.weather import available_dates, pick_day, summarize_day

CET_SUMMER = 2 * 3600  # Europe/Zagreb ljeti (UTC+2)


def slot(utc: str, temp: float, pop: float = 0.0, wind: float = 2.0, desc: str = "vedro", icon: str = "01d"):
    dt = int(datetime.fromisoformat(utc).replace(tzinfo=timezone.utc).timestamp())
    return {
        "dt": dt,
        "dt_txt": utc.replace("T", " "),
        "main": {"temp_min": temp - 1, "temp_max": temp + 1, "feels_like": temp, "humidity": 60},
        "wind": {"speed": wind},
        "pop": pop,
        "weather": [{"description": desc, "icon": icon}],
    }


def forecast(*slots, tz=CET_SUMMER):
    return {"city": {"timezone": tz}, "list": list(slots)}


def test_pick_day_uses_city_local_time():
    # 23:00 UTC 20.10. je 01:00 lokalno 21.10. -> pripada 21.10.
    fc = forecast(slot("2026-10-20T21:00:00", 10), slot("2026-10-20T23:00:00", 8), slot("2026-10-21T11:00:00", 15))
    assert [s["main"]["feels_like"] for s in pick_day(fc, date(2026, 10, 21))] == [8, 15]
    assert available_dates(fc) == [date(2026, 10, 20), date(2026, 10, 21)]


def test_summarize_day_aggregates_whole_day():
    slots = [
        slot("2026-10-21T02:00:00", 5, pop=0.1),
        slot("2026-10-21T11:00:00", 16, pop=0.7, wind=9.3, desc="kiša", icon="10d"),  # 13 h lokalno
        slot("2026-10-21T17:00:00", 11, wind=4),
    ]
    s = summarize_day(slots, CET_SUMMER)
    assert s["min"] == 4 and s["max"] == 17         # preko cijelog dana, ne samo jedan slot
    assert s["pop"] == 70 and s["wind"] == 9.3        # najgori slučaj u danu
    assert s["desc"] == "kiša" and s["icon"] == "10d" and s["feels"] == 16  # slot oko podneva
    assert s["uv"] is None
