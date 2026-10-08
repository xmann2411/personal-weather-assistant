import json
import logging

import httpx
from pydantic import ValidationError

from config import GROQ_API_KEY, GROQ_MODELS
from models import PlanPayload

log = logging.getLogger(__name__)

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class AIUnavailable(Exception):
    """AI plan se ne može dobiti (nema ključa, greška API-ja ili neispravan odgovor)."""


SYSTEM_PROMPT = """
Ti si osobni asistent za vremensku prognozu. Analiziraj vremenske uvjete i vrati praktične savjete.
Odgovaraj na hrvatskom jeziku.
Vrati ISKLJUČIVO ispravan JSON objekt (bez markdowna i dodatnog teksta) ove strukture:
{
  "outfit": {"top": "", "bottom": "", "outerwear": "", "shoes": "", "accessories": [""]},
  "activities": [{"name": "", "indoor": false, "timeSuggestion": "morning|afternoon|evening", "note": ""}],
  "alerts": [{"type": "rain|wind|uv|cold|heat|snow", "message": ""}],
  "packing": [""],
  "rationale": "Kratko objašnjenje (1-3 rečenice)."
}

Pravila:
- Ako je vjerojatnost oborina > 50% → predloži vodootpornu jaknu i obuću te kišobran, i dodaj alert "rain".
- Ako je vjetar > 8 m/s → upozori na bicikliranje/pješačenje, preporuči vjetrootpornu odjeću i dodaj alert "wind".
- Ako je UV indeks >= 6 → predloži kremu sa SPF 30+ i kapu/šešir te dodaj alert "uv". Ako je UV nepoznat, ne izmišljaj ga.
- Ako je maksimalna temperatura >= 30 °C dodaj alert "heat"; ako je minimalna <= 0 °C dodaj alert "cold".
- Ako je u opisu snijeg, dodaj alert "snow".
- Ako nema razloga za upozorenje, "alerts" je prazna lista.
- Predloži 3-4 aktivnosti prilagođene vremenu i odabranom gradu (konkretna mjesta u tom gradu kad ih znaš).
  Kad je kišovito ili vjetrovito, prednost daj aktivnostima u zatvorenom.
- Poštuj preferencije korisnika ako su navedene.
- timeSuggestion mora biti točno jedna od vrijednosti: morning, afternoon, evening.

Primjeri aktivnosti:
- Zagreb: šetnja Gornjim gradom, Muzej Mimara, kava u Tkalčićevoj, šetnja Sljemenom
- Split: Dioklecijanova palača, šetnja Rivom, izlet na Marjan
- Dubrovnik: šetnja zidinama, stari grad, žičara do Srđa
- Samobor: šetnja centrom, stari grad Samobor, degustacija kremšnite

Primjer odgovora (Split, vedro, min 25 °C / max 33 °C, vjetar 5 m/s, kiša 0%, UV 9):
{"outfit": {"top": "lagana pamučna majica", "bottom": "kratke hlače", "outerwear": "nije potrebna", "shoes": "sandale", "accessories": ["sunčane naočale", "šešir"]},
 "activities": [{"name": "Dioklecijanova palača", "indoor": false, "timeSuggestion": "morning", "note": "obiđi prije najveće vrućine"},
                {"name": "izlet na Marjan", "indoor": false, "timeSuggestion": "evening", "note": "hlad borove šume i pogled na zalazak"}],
 "alerts": [{"type": "uv", "message": "Vrlo visok UV indeks; koristi SPF 30+ i nosi šešir."}, {"type": "heat", "message": "Vrućina do 33 °C; pij dovoljno vode i izbjegavaj sunce oko podneva."}],
 "packing": ["krema za sunčanje", "boca vode", "ručnik za plažu"],
 "rationale": "Vruće i sunčano vrijeme s visokim UV indeksom traži laganu odjeću i zaštitu od sunca; aktivnosti su smještene u jutro i večer."}
""".strip()


def build_messages(city: str, date: str, summary: dict, prefs: dict | None) -> list[dict]:
    uv = summary.get("uv")
    uv_text = f"{uv}" if uv is not None else "nepoznat"
    context = (
        f"Grad: {city}\nDatum: {date}\n"
        f"Vrijeme: {summary['desc']}, minimalna {summary['min']} °C, maksimalna {summary['max']} °C, "
        f"subjektivni osjećaj {summary['feels']} °C, vjetar do {summary['wind']} m/s, "
        f"vjerojatnost oborina {summary['pop']}%, UV indeks {uv_text}, vlažnost zraka {summary['humidity']}%.\n"
        f"Preferencije korisnika: {json.dumps(prefs or {}, ensure_ascii=False)}"
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": context},
    ]


def extract_json(text: str) -> dict:
    """Izvlači JSON objekt iz odgovora modela (tolerira ```json ograde i tekst oko JSON-a)."""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("U odgovoru modela nema JSON objekta")
    return json.loads(text[start:end + 1])


async def _call_model(client: httpx.AsyncClient, model: str, messages: list[dict]) -> PlanPayload:
    resp = await client.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": model,
            "temperature": 0.4,
            "max_tokens": 1200,
            "response_format": {"type": "json_object"},
            "messages": messages,
        },
    )
    resp.raise_for_status()
    text = resp.json()["choices"][0]["message"]["content"]
    return PlanPayload.model_validate(extract_json(text))


async def generate_plan(messages: list[dict]) -> PlanPayload:
    if not GROQ_API_KEY:
        raise AIUnavailable("GROQ_API_KEY nije postavljen")

    async with httpx.AsyncClient(timeout=30) as client:
        for model in GROQ_MODELS:
            try:
                return await _call_model(client, model, messages)
            except httpx.HTTPStatusError as e:
                status = e.response.status_code
                log.warning("Groq model %s returned HTTP %s: %s", model, status, e.response.text[:200])
                if status in (401, 403):
                    break  # neispravan ključ - drugi model neće pomoći
            except (httpx.RequestError, ValueError, KeyError, ValidationError) as e:
                # json.JSONDecodeError je podklasa ValueError
                log.warning("Groq model %s failed: %s", model, e)
    raise AIUnavailable("Nijedan Groq model nije vratio ispravan plan")
