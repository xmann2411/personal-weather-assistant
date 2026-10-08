// Datumi po lokalnom vremenu (toISOString je UTC pa iza ponoći "danas" ispadne jučer)
export function toLocalISODate(d: Date): string {
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

export function addDays(d: Date, days: number): Date {
  const copy = new Date(d);
  copy.setDate(copy.getDate() + days);
  return copy;
}

export function formatDateHr(iso: string): string {
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(y, m - 1, d).toLocaleDateString("hr-HR", {
    weekday: "long", day: "numeric", month: "long", year: "numeric",
  });
}
