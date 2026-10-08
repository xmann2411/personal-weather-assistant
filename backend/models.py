from datetime import date as Date
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class PlanIn(BaseModel):
    city: str = Field(min_length=1, max_length=100)
    date: Date                 # "YYYY-MM-DD"
    preferences: Optional[Dict[str, Any]] = None

class WeatherSummary(BaseModel):
    min: float; max: float; feels: float; wind: float
    pop: int; humidity: int; desc: str
    uv: Optional[float] = None          # None ako UV nije dostupan
    icon: Optional[str] = None

class Location(BaseModel):
    name: str
    country: Optional[str] = None
    lat: float
    lon: float

class Outfit(BaseModel):
    top: str; bottom: str; outerwear: str; shoes: str
    accessories: List[str] = []

class Activity(BaseModel):
    name: str
    indoor: bool
    timeSuggestion: str = ""
    note: str = ""

class Alert(BaseModel):
    type: str; message: str

class PlanPayload(BaseModel):
    outfit: Outfit
    activities: List[Activity]
    alerts: List[Alert] = []
    packing: List[str] = []
    rationale: str = ""

class PlanOut(BaseModel):
    location: Location
    date: Date
    weather: WeatherSummary
    plan: PlanPayload
    source: Literal["ai", "fallback"]   # odakle je plan: Groq LLM ili rule-based
