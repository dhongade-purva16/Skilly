import apiClient from './apiClient';

export interface AchieverContext {
  student: {
    full_name: string | null;
    phone: string | null;
    location: string | null;
    bio: string | null;
  };
  academic: {
    degree: string | null;
    branch: string | null;
    academic_year: string | null;
    graduation_year: number | null;
  };
  professional: {
    headline: string | null;
    current_status: string | null;
    experience_level: string | null;
    years_of_experience: number | null;
    professional_summary: string | null;
    work_domain: string | null;
  };
  target: {
    target_company: { id: number; name: string; description: string | null } | null;
    target_role: { id: number; name: string; description: string | null } | null;
    career_role: { id: number; name: string; description: string | null } | null;
  };
  external_profiles: {
    github_status: string;
    github_url: string | null;
    linkedin_status: string;
    linkedin_url: string | null;
    portfolio_status: string;
    portfolio_url: string | null;
  };
  resume: {
    filename: string | null;
    mime_type: string | null;
    file_size: number | null;
    upload_date: string | null;
    active_status: boolean;
    extraction_status: string;
    extracted_text: string | null;
  };
  evidence: Array<{
    type: string;
    status: string;
    title: string | null;
    metadata: any;
    created_at: string | null;
    updated_at: string | null;
  }>;
  skills: Array<{
    skill: { id: number; name: string; category: { id: number; name: string } };
    proficiency_level: number;
    source_status: string | null;
    updated_timestamp: string | null;
  }>;
  skill_gaps: Array<{
    skill: { id: number; name: string; category: { id: number; name: string } };
    required_proficiency: number;
    current_proficiency: number;
    status: string;
    requirement_source: string;
  }>;
  requirements: Array<{
    skill: { id: number; name: string; category: { id: number; name: string } };
    required_proficiency: number;
    source: string;
  }>;
  metadata: {
    context_version: string;
    generated_at: string;
    requirement_source: string;
    available_evidence_count: number;
    verified_evidence_count: number;
    unverified_evidence_count: number;
    has_resume: boolean;
    has_resume_text: boolean;
    has_github: boolean;
    has_linkedin: boolean;
    has_portfolio: boolean;
    has_assessment: boolean;
    has_target_company: boolean;
    has_target_role: boolean;
  };
}

export const getAchieverContext = async (): Promise<AchieverContext> => {
  const response = await apiClient.get<AchieverContext>('/api/v1/student/achiever/context');
  return response.data;
};

export interface EvidenceSummaryItem {
  source: string;
  status: string;
}

export interface PrioritizedSkillGap {
  skill: { id: number; name: string; category: { id: number; name: string } };
  required_proficiency: number;
  current_proficiency: number;
  gap_status: string;
  priority: string;
  requirement_source: string;
  evidence_summary: EvidenceSummaryItem[];
  dependency_status: string;
  reasons: string[];
}

export interface AchieverPriorityResponse {
  target: any; // We can type this fully if needed, same as in AchieverContext
  requirement_source: string;
  prioritized_gaps: PrioritizedSkillGap[];
  summary: string;
}

export const getAchieverPriorities = async (): Promise<AchieverPriorityResponse> => {
  const response = await apiClient.get<AchieverPriorityResponse>('/api/v1/student/achiever/priorities');
  return response.data;
};

export interface KnowledgeResourceResponse {
  resource_id: number;
  title: string;
  resource_type: string;
  provider: string;
  difficulty: string | null;
  source_url: string;
  estimated_duration: string | null;
  similarity_score: number;
}

export interface SkillResourceGroup {
  skill_id: number;
  skill_name: string;
  priority: string;
  resources: KnowledgeResourceResponse[];
}

export interface AchieverResourcesResponse {
  student_id: number;
  target: {
    company: string;
    role: string;
  };
  resources: SkillResourceGroup[];
}

export const getAchieverResources = async (): Promise<AchieverResourcesResponse> => {
  const response = await apiClient.get<AchieverResourcesResponse>('/api/v1/student/achiever/resources');
  return response.data;
};

export interface RoadmapResource {
  resource_id: number;
  title: string;
  source_url: string;
  difficulty?: string;
  provider?: string;
}

export interface RoadmapStep {
  id: number;
  roadmap_id: number;
  step_order: number;
  skill_id: number;
  skill_name: string;
  priority: string;
  objective: string;
  description?: string;
  estimated_duration?: string;
  resources: RoadmapResource[];
  practice_task?: string;
  status: string;
}

export interface RoadmapResponse {
  roadmap_id: number;
  target: {
    company?: string;
    role?: string;
  };
  summary?: string;
  status: string;
  steps: RoadmapStep[];
}

export const getRoadmap = async (): Promise<RoadmapResponse | null> => {
  try {
    const response = await apiClient.get<RoadmapResponse>('/api/v1/student/achiever/roadmap');
    return response.data;
  } catch (error: any) {
    if (error.response && error.response.status === 404) {
      return null;
    }
    throw error;
  }
};

export const generateRoadmap = async (): Promise<RoadmapResponse> => {
  const response = await apiClient.post<RoadmapResponse>('/api/v1/student/achiever/roadmap/generate');
  return response.data;
};
