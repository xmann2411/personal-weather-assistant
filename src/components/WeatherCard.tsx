import { Location, WeatherSummary } from "../types/plan";

export default function WeatherCard({ location, date, weather }:{
  location: Location; date: string; weather: WeatherSummary;
}) {
  return (
    <section style={{ border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
      <strong>{location.name}{location.country ? `, ${location.country}` : ""} — {date}</strong>
      <div>{weather.desc}, min {Math.round(weather.min)}°C / max {Math.round(weather.max)}°C, vjetar {weather.wind} m/s, kiša {weather.pop}%</div>
    </section>
  );
}
