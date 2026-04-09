import { ScanResponse } from "@/types/setup";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export async function getSetups(): Promise<ScanResponse> {
  const response = await fetch(`${API_BASE}/v1/scan`, { next: { revalidate: 60 } });
  if (!response.ok) {
    throw new Error("Failed to fetch setups");
  }
  return response.json();
}
