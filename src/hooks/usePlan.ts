import { useState } from "react";
import { BuildPlanInput, buildPlan } from "../services/plan.service";
import { PlanResponse } from "./../types/plan";

export function usePlan() {
  const [data, setData] = useState<PlanResponse|null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string|null>(null);

  const submit = async (input: BuildPlanInput) => {
    setLoading(true); setError(null);
    try { setData(await buildPlan(input)); }
    catch (e:any) { setError(e.message ?? "Greška pri dohvaćanju plana."); setData(null); }
    finally { setLoading(false); }
  };

  return { data, loading, error, submit };
}
