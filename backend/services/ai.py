import os, json, httpx
from dotenv import load_dotenv
load_dotenv()
GROQ=os.getenv("GROQ_API_KEY")

def build_prompt(city, date, summary: dict, prefs: dict):
    return f"""
Ti si osobni asistent za vremensku prognozu. Analiziraj vremenske uvjete i vrati praktične savjete.  
Odgovaraj na hrvatskom jeziku.  
Vrati ISKLJUČIVO ispravan JSON koji odgovara ovoj strukturi:
{{
  "outfit": {{"top":"","bottom":"","outerwear":"","shoes":"","accessories":[]}},
  "activities": [{{"name":"","indoor":false,"timeSuggestion":"morning|afternoon|evening","note":""}}],
  "alerts": [{{"type":"rain|wind|uv|cold|heat|snow","message":""}}],
  "packing": ["stavka1","stavka2"],
  "rationale": "Kratko objašnjenje."
}}

*Kontekst:*
- Grad: {city}, Datum: {date}
- Vrijeme (°C): minimalna {summary["min"]}, maksimalna {summary["max"]}, subjektivni osjećaj {summary["feels"]},  
  vjetar {summary["wind"]} m/s, vjerojatnost oborina {summary["pop"]}%, UV indeks {summary["uv"]},  
  vlažnost zraka {summary["humidity"]}%, stanje "{summary["desc"]}".
- Preferencije korisnika: {json.dumps(prefs or {})}

*Pravila:*
- Ako je vjerojatnost oborina > 50% → predloži vodootpornu jaknu i obuću, te kišobran.
- Ako je vjetar > 8 m/s → upozori na bicikliranje/pješačenje; preporuči vjetrootpornu odjeću.
- Ako je UV indeks > 6 → predloži korištenje kreme sa SPF 30+ i nošenje kape/šešira.
- Aktivnosti trebaju odgovarati vremenskim uvjetima; kad je kišovito ili vjetrovito, predloži aktivnosti u zatvorenom prostoru.
- Preporučiti aktivnosti s obzirom na grad koji je odabran. 

*Ideje za aktivnosti:*
Aktivnosti u Zagrebu: šetnja Gornjim gradom, posjet Muzeju Mimara, kava u Tkalčićevoj ulici, šetnja po Sljemenu
Aktivnosti u Splitu: posjet Dioklecijanovoj palači, šetnja Riva šetnicom, izlet na Marjan.
Aktivnosti u Dubrovniku: šetnja zidinama, posjet starom gradu, vožnja žičarom do Srđa.
Aktivnosti u Samoboru: šetnja centrom grada, posjet dvorcu Samobor, degustacija kremšnite.

*Primjeri:*
**Primjer 1:**
Zagreb, HR — 2025-10-21
slaba kiša, min 9°C / max 11°C, vjetar 0.78 m/s, kiša 44%
Preporuka za odjeću: majica dugih rukava, traperice, vodootporna jakna, vodootporne cipele ili čizme, kišobran
Preporučene aktivnosti: posjet Muzeju Mimara, kava u Tkalčićevoj ulici, shopping u Arena Centru
Upozorenja: velika šansa kiše; ponesi kišobran i vodootpornu obuću.
Spakiraj: kišobran, rezervne čarape, punjač za telefon
Zašto ove preporuke: Prognoza pokazuje slabu kišu tijekom dana, stoga je važno biti pripremljen za mokre uvjete. Aktivnosti u zatvorenom prostoru su idealne za ovaj dan.

**Primjer 2:**
Split, HR — 2025-07-15
vedro, min 25°C / max 33°C, vjetar 5.14 m/s, kiša 0%, UV indeks 9
Preporuka za odjeću: lagana majica, kratke hlače, sandale, sunčane naočale, kapa ili šešir
Preporučene aktivnosti: posjet Dioklecijanovoj palači, šetnja Rivom, izlet na Marjan
Upozorenja: visoki UV indeksi; koristi kremu sa SPF 30+ i nosi kapu ili šešir.
Spakiraj: krema za sunčanje, voda, ručnik za plažu
Zašto ove preporuke: Vruće i sunčano vrijeme s visokim UV indeksom zahtijeva laganu odjeću i zaštitu od sunca. Aktivnosti na otvorenom su savršene za uživanje u lijepom vremenu.
"""

async def call_groq(prompt: str):
    async def call_groq_with_model(model_name: str, prompt: str):
        headers = {"Authorization": f"Bearer {GROQ}", "Content-Type": "application/json"}
        body = {
            "model": model_name,
            "temperature": 0.4,
            "max_tokens": 600,
            "messages": [{"role": "user", "content": prompt}],
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=body,
            )
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"].strip()
            if text.startswith("```"):
                text = text.strip("`").split("json")[-1].strip()
            return json.loads(text)

    try:
        # Pokušaj s glavnim modelom
        return await call_groq_with_model("llama-3.3-70b-versatile", prompt)
    except httpx.HTTPStatusError as e:
        # Ako prvi model javlja 400 — probaj alternativni
        if e.response is not None and e.response.status_code == 400:
            print("Model decommissioned, switching to llama-3.1-8b-instant")
            return await call_groq_with_model("llama-3.1-8b-instant", prompt)
        raise

