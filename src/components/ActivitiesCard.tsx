import { Activity } from "../types/plan";

interface Props {
  activities: Activity[];
}

export default function ActivitiesCard({ activities }: Props) {
  return (
    <section style={{ border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
      <h3>Preporučene aktivnosti</h3>
      {activities.length === 0 ? (
        <p>Nema preporučenih aktivnosti za odabrani dan.</p>
      ) : (
        <ul style={{ listStyleType: "disc", paddingLeft: 16 }}>
          {activities.map((a, i) => (
            <li key={i}>
              <strong>{a.name}</strong> — {a.indoor ? "unutarnja" : "vanjska"} aktivnost
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
