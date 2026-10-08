import { Activity } from "../types/plan";

const TIME_LABELS: Record<string, string> = {
  morning: "ujutro",
  afternoon: "poslijepodne",
  evening: "navečer",
};

interface Props {
  activities: Activity[];
}

export default function ActivitiesCard({ activities }: Props) {
  return (
    <section className="card">
      <h3>Preporučene aktivnosti</h3>
      {activities.length === 0 ? (
        <p>Nema preporučenih aktivnosti za odabrani dan.</p>
      ) : (
        <ul>
          {activities.map((a, i) => (
            <li key={i}>
              <strong>{a.name}</strong>{" "}
              <span className="muted">
                ({a.indoor ? "unutra" : "vani"}
                {TIME_LABELS[a.timeSuggestion] ? `, ${TIME_LABELS[a.timeSuggestion]}` : ""})
              </span>
              {a.note && <div className="muted small">{a.note}</div>}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
