import { Alert } from "../types/plan";

const ALERT_LABELS: Record<string, string> = {
  rain: "🌧️ Kiša",
  wind: "💨 Vjetar",
  uv: "☀️ UV",
  cold: "🥶 Hladnoća",
  heat: "🔥 Vrućina",
  snow: "❄️ Snijeg",
};

interface Props {
  alerts: Alert[];
}

export default function AlertsCard({ alerts }: Props) {
  return (
    <section className={`card${alerts.length ? " card-warning" : ""}`}>
      <h3>Upozorenja</h3>
      {alerts.length === 0 ? (
        <p>Nema posebnih upozorenja 🌤️</p>
      ) : (
        <ul>
          {alerts.map((alert, i) => (
            <li key={i}>
              <strong>{ALERT_LABELS[alert.type] ?? alert.type}</strong>: {alert.message}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
