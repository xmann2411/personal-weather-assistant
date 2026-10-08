import pytest

from services.ai import build_messages, extract_json
from services.fallback import rule_based_plan

BASE = dict(min=12, max=18, feels=15, wind=3, pop=10, uv=None, humidity=60, desc="vedro", icon="01d")


def test_extract_json_handles_fences_and_word_json():
    text = '```json\n{"rationale": "json format je ok", "packing": []}\n```'
    assert extract_json(text) == {"rationale": "json format je ok", "packing": []}


def test_extract_json_rejects_non_json():
    with pytest.raises(ValueError):
        extract_json("Nažalost ne mogu pomoći.")


def test_build_messages_marks_unknown_uv():
    user = build_messages("Zagreb, HR", "2026-10-21", BASE, {"notes": "volim muzeje"})[1]["content"]
    assert "UV indeks nepoznat" in user
    assert "volim muzeje" in user


def test_fallback_outfit_depends_on_temperature():
    cold = rule_based_plan({**BASE, "feels": -4, "min": -6, "max": 1})
    hot = rule_based_plan({**BASE, "feels": 31, "min": 22, "max": 34, "uv": 8})
    assert cold.outfit.outerwear == "zimska jakna"
    assert hot.outfit.shoes == "sandale"
    assert {a.type for a in cold.alerts} == {"cold"}
    assert {a.type for a in hot.alerts} == {"heat", "uv"}


def test_fallback_rain_and_wind_prefer_indoor():
    plan = rule_based_plan({**BASE, "pop": 80, "wind": 10})
    assert "kišobran" in plan.outfit.accessories
    assert {a.type for a in plan.alerts} == {"rain", "wind"}
    assert all(a.indoor for a in plan.activities)
