import os
from pathlib import Path

from dotenv import load_dotenv

# .env se uvijek čita iz backend/ mape, neovisno o tome odakle je server pokrenut
load_dotenv(Path(__file__).parent / ".env")

OWM_KEY = os.getenv("OWM_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Prvi model je glavni, ostali su rezerva (npr. ako Groq ukine model)
GROQ_MODELS = [
    m.strip()
    for m in os.getenv("GROQ_MODELS", "llama-3.3-70b-versatile,llama-3.1-8b-instant").split(",")
    if m.strip()
]

CORS_ORIGINS = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    if o.strip()
]
