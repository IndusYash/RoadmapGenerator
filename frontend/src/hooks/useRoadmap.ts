import { useState, useCallback } from 'react';
import type { InputFormData, RoadmapResponse } from '../types';
import { generateRoadmap } from '../services/api';

const defaultForm: InputFormData = {
  name: '',
  icp_type: 'ICP-A',
  current_role: '',
  target_role: '',
  urgency_months: 6,
  skills: [],
  experience_months: 0,
  language: 'en',
  location: '',
};

export function useRoadmap() {
  const [form, setForm] = useState<InputFormData>(defaultForm);
  const [loading, setLoading] = useState(false);
  const [roadmap, setRoadmap] = useState<RoadmapResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const updateField = useCallback(<K extends keyof InputFormData>(key: K, value: InputFormData[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  }, []);

  const submit = useCallback(async () => {
    setLoading(true);
    setError(null);
    setRoadmap(null);

    try {
      const result = await generateRoadmap(form);
      setRoadmap(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [form]);

  const reset = useCallback(() => {
    setForm(defaultForm);
    setRoadmap(null);
    setError(null);
  }, []);

  return { form, updateField, loading, roadmap, error, submit, reset };
}
