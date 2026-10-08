import { Location, WeatherSummary } from "../types/plan";
import { formatDateHr } from "../utils/date";

export default function WeatherCard({ location, date, weather }:{
  location: Location; date: string; weather: WeatherSummary;
}) {
  return (
    <section className="card weather-card">
      <div className="weather-head">
        {weather.icon && (
          <img
            src={`https://openweathermap.org/img/wn/${weather.icon}@2x.png`}
            alt="" width={64} height={64}
          />
        )}
        <div>
          <h2>{location.name}{location.country ? `, ${location.country}` : ""}</h2>
          <div className="muted">{formatDateHr(date)} · {weather.desc}</div>
        </div>
        <div className="temps">
          <strong>{Math.round(weather.max)}°</strong> / {Math.round(weather.min)}°C
        </div>
      </div>
      <ul className="weather-stats">
        <li><span>Osjećaj</span>{Math.round(weather.feels)}°C</li>
        <li><span>Vjetar</span>do {weather.wind} m/s</li>
        <li><span>Kiša</span>{weather.pop}%</li>
        <li><span>Vlažnost</span>{weather.humidity}%</li>
        <li><span>UV indeks</span>{weather.uv ?? "n/a"}</li>
      </ul>
    </section>
  );
}
