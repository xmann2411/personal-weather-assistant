import { Alert } from "../types/plan";

interface Props {
  alerts: Alert[];
}

export default function AlertsCard({ alerts }: Props) {
  if (alerts.length === 0) {
    return (
      <section style={{ border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
        <h3>Upozorenja</h3>
        <p>Nema posebnih upozorenja 🌤️</p>
      </section>
    );
  }

  return (
    <section style={{ border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
      <h3>Upozorenja</h3>
      <ul style={{ listStyleType: "disc", paddingLeft: 16 }}>
        {alerts.map((alert, i) => (
          <li key={i}>
            <strong>{alert.type.toUpperCase()}</strong>: {alert.message}
          </li>
        ))}
      </ul>
    </section>
  );
}
