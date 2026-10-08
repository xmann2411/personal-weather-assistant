"""Rule-based plan kad AI (Groq) nije dostupan.

Pravila prate ona iz AI prompta, tako da korisnik dobije smislen plan i bez LLM-a.
"""
from models import PlanPayload


def _outfit_for(temp: float) -> dict:
    if temp < 0:
        return {"top": "termo majica i topli džemper", "bottom": "tople hlače", "outerwear": "zimska jakna",
                "shoes": "zimske čizme", "accessories": ["kapa", "šal", "rukavice"]}
    if temp < 10:
        return {"top": "džemper", "bottom": "traperice", "outerwear": "topla jakna",
                "shoes": "zatvorene cipele", "accessories": ["šal"]}
    if temp < 18:
        return {"top": "majica dugih rukava", "bottom": "traperice", "outerwear": "lagana jakna",
                "shoes": "udobne tenisice", "accessories": []}
    if temp < 26:
        return {"top": "majica kratkih rukava", "bottom": "lagane hlače", "outerwear": "nije potrebna",
                "shoes": "tenisice", "accessories": ["sunčane naočale"]}
    return {"top": "lagana pamučna majica", "bottom": "kratke hlače", "outerwear": "nije potrebna",
            "shoes": "sandale", "accessories": ["sunčane naočale", "šešir"]}


def rule_based_plan(summary: dict) -> PlanPayload:
    temp = summary["feels"]
    rainy = summary["pop"] > 50
    windy = summary["wind"] > 8
    uv = summary.get("uv")
    snowy = (summary.get("icon") or "").startswith("13")

    outfit = _outfit_for(temp)
    alerts, packing = [], ["boca vode", "punjač za mobitel"]

    if rainy:
        outfit["outerwear"] = "vodootporna jakna"
        outfit["shoes"] = "vodootporna obuća"
        outfit["accessories"] = [*outfit["accessories"], "kišobran"]
        alerts.append({"type": "rain", "message": f"Vjerojatnost kiše {summary['pop']}%; ponesi kišobran i vodootpornu obuću."})
        packing.append("rezervne čarape")
    if windy:
        alerts.append({"type": "wind", "message": f"Vjetar do {summary['wind']} m/s; izbjegavaj bicikl i izložena mjesta."})
    if uv is not None and uv >= 6:
        alerts.append({"type": "uv", "message": f"UV indeks {uv}; koristi kremu SPF 30+ i nosi kapu ili šešir."})
        packing.append("krema za sunčanje SPF 30+")
    if summary["max"] >= 30:
        alerts.append({"type": "heat", "message": f"Vrućina do {round(summary['max'])} °C; pij dovoljno vode."})
    if summary["min"] <= 0:
        alerts.append({"type": "cold", "message": f"Temperatura pada do {round(summary['min'])} °C; moguća poledica."})
    if snowy:
        alerts.append({"type": "snow", "message": "Očekuje se snijeg; obuj obuću s dobrim gazištem."})

    if rainy or windy or snowy:
        activities = [
            {"name": "posjet muzeju ili galeriji", "indoor": True, "timeSuggestion": "morning", "note": "zaklon od lošeg vremena"},
            {"name": "kava ili ručak u omiljenom kafiću", "indoor": True, "timeSuggestion": "afternoon", "note": ""},
            {"name": "kino ili kazalište", "indoor": True, "timeSuggestion": "evening", "note": ""},
        ]
    else:
        activities = [
            {"name": "šetnja centrom grada", "indoor": False, "timeSuggestion": "morning", "note": ""},
            {"name": "boravak u parku ili prirodi", "indoor": False, "timeSuggestion": "afternoon",
             "note": "izbjegavaj sunce oko podneva" if summary["max"] >= 28 else ""},
            {"name": "večernja šetnja", "indoor": False, "timeSuggestion": "evening", "note": ""},
        ]

    return PlanPayload.model_validate({
        "outfit": outfit,
        "activities": activities,
        "alerts": alerts,
        "packing": packing,
        "rationale": "AI servis trenutno nije dostupan pa su preporuke generirane jednostavnim pravilima "
                     "na temelju temperature, kiše, vjetra i UV indeksa.",
    })
