import { useState } from "react";
import { BuildPlanInput } from "../services/plan.service";

export default function SearchForm({ onSubmit, disabled }:{
  onSubmit: (i: BuildPlanInput) => void;
  disabled?: boolean;
}) {
  const [city, setCity] = useState(localStorage.getItem("city") || "");
  const [date, setDate] = useState("");

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!city || !date) return;
    localStorage.setItem("city", city.trim());
    onSubmit({ city: city.trim(), date });
  };

  const today = new Date().toISOString().slice(0,10);
  const max = new Date(Date.now() + 4*24*60*60*1000).toISOString().slice(0,10);

  return (
    <form onSubmit={submit} style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
      <input
        placeholder="Grad (npr. Zagreb)"
        value={city}
        onChange={(e)=>setCity(e.target.value)}
        style={{ padding: 8, border: "1px solid #ddd", borderRadius: 6, flex: "1 1 220px" }}
      />
      <input
        type="date" value={date} min={today} max={max}
        onChange={(e)=>setDate(e.target.value)}
        style={{ padding: 8, border: "1px solid #ddd", borderRadius: 6 }}
      />
      <button disabled={disabled} style={{ padding: "8px 14px", borderRadius: 6 }}>
        {disabled ? "Generiram..." : "Generiraj plan"}
      </button>
    </form>
  );
}
