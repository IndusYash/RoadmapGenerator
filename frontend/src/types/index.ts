// TypeScript interfaces matching the Python backend schemas

export type ICPType = 'ICP-A' | 'ICP-B';
export type Language = 'en' | 'hi';
export type BlurLevel = 0 | 1 | 2 | 3;

export interface InputFormData {
  name: string;
  icp_type: ICPType;
  current_role: string;
  target_role: string;
  urgency_months: number;
  skills: string[];
  experience_months: number;
  language: Language;
  location: string;
}

export interface Milestone {
  code: string; // M01 – M07
  title: string;
  phase: number; // 1–4
  target_month: number;
  expected_completion: string;
  estimated_duration_weeks: number;
  salary_tier: string;
  unlock_statement: string;
  blur_level: BlurLevel;
  scenario_count: number;
  assessment_count: number;
  mock_interview_count: number;
}

export interface RoadmapResponse {
  milestones: Milestone[];
}
