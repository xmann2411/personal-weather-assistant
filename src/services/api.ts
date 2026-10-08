const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// FastAPI vraća detail kao string (HTTPException) ili kao listu grešaka (422 validacija)
function errorMessage(data: any, status: number): string {
  const detail = data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return "Neispravan unos: " + detail.map((d) => d.msg).join("; ");
  return `Greška servera (${status}).`;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      ...options,
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    });
  } catch {
    throw new Error("Backend nije dostupan. Je li pokrenut na " + BASE_URL + "?");
  }

  const text = await res.text();
  let data: any = null;
  try { data = text ? JSON.parse(text) : null; } catch { /* odgovor nije JSON */ }

  if (!res.ok) throw new Error(errorMessage(data, res.status));
  return data as T;
}

export const api = { request };
