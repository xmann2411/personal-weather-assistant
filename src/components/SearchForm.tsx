import { useState } from "react";
import { BuildPlanInput } from "../services/plan.service";
import { addDays, toLocalISODate } from "../utils/date";

const storage = {
  get: (key: string) => { try { return localStorage.getItem(key) || ""; } catch { return ""; } },
  set: (key: string, value: string) => { try { localStorage.setItem(key, value); } catch { /* npr. privatni način */ } },
};

export default function SearchForm({ onSubmit, disabled }:{
  onSubmit: (i: BuildPlanInput) => void;
  disabled?: boolean;
}) {
  const today = toLocalISODate(new Date());
  // OWM 5-day/3-hour prognoza pokriva danas + idućih ~4-5 dana
  const max = toLocalISODate(addDays(new Date(), 4));

  const [city, setCity] = useState(storage.get("city"));
  const [date, setDate] = useState(today);
  const [notes, setNotes] = useState(storage.get("preferences"));

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const c = city.trim();
    if (!c || !date) return;
    storage.set("city", c);
    storage.set("preferences", notes.trim());
    onSubmit({ city: c, date, preferences: notes.trim() ? { notes: notes.trim() } : undefined });
  };

  return (
    <form onSubmit={submit} className="search-form">
      <div className="search-row">
        <label className="field grow">
          <span>Grad</span>
          <input
            placeholder="npr. Zagreb"
            value={city}
            onChange={(e)=>setCity(e.target.value)}
            maxLength={100}
            required
          />
        </label>
        <label className="field">
          <span>Datum</span>
          <input
            type="date" value={date} min={today} max={max}
            onChange={(e)=>setDate(e.target.value)}
            required
          />
        </label>
      </div>
      <label className="field">
        <span>Preferencije (opcionalno)</span>
        <input
          placeholder="npr. putujem s djecom, volim muzeje, osjetljiv/a sam na hladnoću"
          value={notes}
          onChange={(e)=>setNotes(e.target.value)}
          maxLength={300}
        />
      </label>
      <button type="submit" disabled={disabled}>
        {disabled ? "Generiram..." : "Generiraj plan"}
      </button>
    </form>
  );
}
