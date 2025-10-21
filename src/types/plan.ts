export type WeatherSummary = {
  min: number; max: number; feels: number; wind: number;
  pop: number; uv: number; humidity: number; desc: string; icon?: string;
};

export type Outfit = {
  top: string; bottom: string; outerwear: string; shoes: string; accessories: string[];
};

export type Activity = {
  name: string; indoor: boolean; timeSuggestion: "morning"|"afternoon"|"evening"; note: string;
};

export type Alert = { type: "rain"|"wind"|"uv"|"cold"|"heat"|"snow"; message: string };

export type PlanPayload = {
  outfit: Outfit; activities: Activity[]; alerts: Alert[]; packing: string[]; rationale: string;
};

export type Location = { name: string; country?: string };

export type PlanResponse = {
  location: Location; date: string; weather: WeatherSummary; plan: PlanPayload;
};
