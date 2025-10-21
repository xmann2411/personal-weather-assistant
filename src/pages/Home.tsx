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
    <div className="space-y-4">
      <SearchForm onSubmit={submit} disabled={loading} />
      {loading && <div>Učitavanje…</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}

      {data && (
        <>
          <WeatherCard location={data.location} date={data.date} weather={data.weather} />
          <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))" }}>
            <OutfitCard outfit={data.plan.outfit} />
            <ActivitiesCard activities={data.plan.activities} />
            <AlertsCard alerts={data.plan.alerts} />
            <PackingCard items={data.plan.packing} />
            <WhyDetails rationale={data.plan.rationale} />
          </div>
        </>
      )}
    </div>
  );
}
