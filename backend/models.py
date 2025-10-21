from pydantic import BaseModel
from typing import List, Optional

class PlanIn(BaseModel):
    city: str
    date: str                  # "YYYY-MM-DD"
    preferences: Optional[dict] = None

class WeatherSummary(BaseModel):
    min: float; max: float; feels: float; wind: float
    pop: int; uv: int; humidity: int; desc: str
    icon: Optional[str] = None

class Location(BaseModel):
    name: str
    country: Optional[str] = None
    lat: float
    lon: float

class Outfit(BaseModel):
    top: str; bottom: str; outerwear: str; shoes: str; accessories: List[str]

class Activity(BaseModel):
    name: str; indoor: bool; timeSuggestion: str; note: str

class Alert(BaseModel):
    type: str; message: str

class PlanPayload(BaseModel):
    outfit: Outfit
    activities: List[Activity]
    alerts: List[Alert]
    packing: List[str]
    rationale: str

class PlanOut(BaseModel):
    location: Location
    date: str
    weather: WeatherSummary
    plan: PlanPayload
