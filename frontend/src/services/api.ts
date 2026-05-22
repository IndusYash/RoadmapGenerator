import type { InputFormData, RoadmapResponse } from '../types';
import { mockRoadmap } from '../data/mockRoadmap';

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export async function generateRoadmap(data: InputFormData): Promise<RoadmapResponse> {
  try {
    const response = await fetch(`${API_BASE}/generate-roadmap`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown server error' }));
      throw new Error(error.detail ?? `Server error: ${response.status}`);
    }

    return (await response.json()) as RoadmapResponse;
  } catch (err) {
    // If the backend is unreachable, fall back to mock data so the UI is always demoable
    if (err instanceof TypeError && err.message.includes('fetch')) {
      console.warn('[api] Backend unreachable — using mock roadmap data');
      // Simulate a realistic delay
      await new Promise((r) => setTimeout(r, 2200));
      return mockRoadmap;
    }
    throw err;
  }
}
