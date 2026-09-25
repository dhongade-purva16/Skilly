import apiClient from './apiClient';
import { type Skill } from './skill';

export interface AssessmentQuestion {
  id: number;
  question_text: string;
  options: string[];
  difficulty: number;
}

export interface Assessment {
  id: number;
  title: string;
  description?: string;
  skill_id: number;
  skill: Skill;
  target_company_id?: number;
  assessment_source?: 'company_specific' | 'role_fallback' | string;
  target_company_name?: string;
}

export interface AssessmentDetail extends Assessment {
  questions: AssessmentQuestion[];
}

export interface AssessmentAnswer {
  question_id: number;
  selected_option_index: number;
}

export interface AssessmentSubmission {
  answers: AssessmentAnswer[];
}

export interface AssessmentResult {
  id: number;
  assessment_id: number;
  score: number;
  started_at: string;
  completed_at: string;
}

export const getAssessments = async () => {
  const { data } = await apiClient.get<Assessment[]>('/api/v1/assessments');
  return data;
};

export const getAssessment = async (id: number) => {
  const { data } = await apiClient.get<AssessmentDetail>(`/api/v1/assessments/${id}`);
  return data;
};

export const startAttempt = async (assessmentId: number) => {
  const { data } = await apiClient.post<AssessmentResult>(`/api/v1/assessments/${assessmentId}/attempt`);
  return data;
};

export const submitAttempt = async (attemptId: number, submission: AssessmentSubmission) => {
  const { data } = await apiClient.post<AssessmentResult>(`/api/v1/assessments/attempt/${attemptId}/submit`, submission);
  return data;
};
