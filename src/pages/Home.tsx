import { usePlan } from "../hooks/usePlan";
import SearchForm from "../components/SearchForm";
import WeatherCard from "../components/WeatherCard";
import OutfitCard from "../components/OutfitCard";
import ActivitiesCard from "../components/ActivitiesCard";
import AlertsCard from "../components/AlertsCard";
import PackingCard from "../components/PackingCard";
import WhyDetails from "../components/WhyDetails";

export default function Home() {
  const { data, loading, error, submit } = usePlan();

  return (
    <div className="stack">
      <SearchForm onSubmit={submit} disabled={loading} />
      {loading && <div className="muted" aria-live="polite">Učitavanje…</div>}
      {error && <div className="error" role="alert">{error}</div>}

      {data && (
        <>
          <WeatherCard location={data.location} date={data.date} weather={data.weather} />
          {data.source === "fallback" && (
            <div className="notice">
              AI servis trenutno nije dostupan – prikazane su osnovne preporuke na temelju pravila.
            </div>
          )}
          <div className="card-grid">
            <OutfitCard outfit={data.plan.outfit} />
            <ActivitiesCard activities={data.plan.activities} />
            <AlertsCard alerts={data.plan.alerts} />
            <PackingCard items={data.plan.packing} />
          </div>
          <WhyDetails rationale={data.plan.rationale} />
        </>
      )}
    </div>
  );
}
