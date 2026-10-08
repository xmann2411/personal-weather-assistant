export type WeatherSummary = {
  min: number; max: number; feels: number; wind: number;
  pop: number; uv: number | null; humidity: number; desc: string; icon?: string | null;
};

export type Outfit = {
  top: string; bottom: string; outerwear: string; shoes: string; accessories: string[];
};

export type TimeOfDay = "morning" | "afternoon" | "evening";

export type Activity = {
  // LLM može vratiti i nešto izvan TimeOfDay, pa je tip namjerno širi
  name: string; indoor: boolean; timeSuggestion: TimeOfDay | string; note: string;
};

export type AlertType = "rain" | "wind" | "uv" | "cold" | "heat" | "snow";

export type Alert = { type: AlertType | string; message: string };

export type PlanPayload = {
  outfit: Outfit; activities: Activity[]; alerts: Alert[]; packing: string[]; rationale: string;
};

export type Location = { name: string; country?: string | null; lat: number; lon: number };

export type PlanResponse = {
  location: Location;
  date: string;
  weather: WeatherSummary;
  plan: PlanPayload;
  source: "ai" | "fallback";
};
