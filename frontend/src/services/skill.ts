import apiClient from './apiClient';

export interface SkillCategory {
  id: number;
  name: string;
}

export interface Skill {
  id: number;
  name: string;
  category_id: number;
  category?: SkillCategory;
}

export interface StudentSkill {
  id: number;
  skill_id: number;
  proficiency_level: number;
  score: number;
  confidence: number;
  last_assessed_at?: string;
  skill: Skill;
}

export interface SkillGap {
  skill: Skill;
  required_level: number;
  current_level: number;
  current_score: number;
  gap_status: 'Sufficient' | 'Gap' | 'Missing';
  requirement_source?: 'company_specific' | 'role_fallback' | string;
  target_company_name?: string;
}

export const getStudentSkills = async () => {
  const { data } = await apiClient.get<StudentSkill[]>('/api/v1/student/skills');
  return data;
};

export const getStudentSkillGaps = async () => {
  const { data } = await apiClient.get<SkillGap[]>('/api/v1/student/skill-gaps');
  return data;
};

export const getSkills = async () => {
  const { data } = await apiClient.get<Skill[]>('/api/v1/skills');
  return data;
};

export const getSkillCategories = async () => {
  const { data } = await apiClient.get<SkillCategory[]>('/api/v1/skills/categories');
  return data;
};
