import { PlanResponse } from "../types/plan";
import { api } from "./api";

export type BuildPlanInput = {
  city: string;
  date: string; // YYYY-MM-DD
  preferences?: Record<string, unknown>;
};

export const buildPlan = (payload: BuildPlanInput) =>
  api.request<PlanResponse>("/plan", {
    method: "POST",
    body: JSON.stringify(payload),
  });
