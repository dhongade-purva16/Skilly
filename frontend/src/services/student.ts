import apiClient from './apiClient';

export interface StudentProfile {
  full_name?: string;
  phone?: string;
  location?: string;
  bio?: string;
  gems_enabled?: boolean;
  gems_reminder_enabled?: boolean;
  gems_reminder_time?: string;
}

export interface GemsPreferences {
  gems_enabled?: boolean;
  gems_reminder_enabled?: boolean;
  gems_reminder_time?: string;
}

export interface AcademicProfile {
  degree?: string;
  branch?: string;
  academic_year?: string;
  graduation_year?: number;
}

export interface ProfessionalProfile {
  headline?: string;
  current_status?: string;
  experience_level?: string;
  years_of_experience?: number;
  professional_summary?: string;
  work_domain?: string;
}

export interface ExternalProfiles {
  github_url?: string;
  linkedin_url?: string;
  portfolio_url?: string;
  linkedin_sync_status?: string;
}

export interface StudentResume {
  id: number;
  student_id: number;
  filename: string;
  file_size: number;
  content_type: string;
  uploaded_at: string;
  is_active: boolean;
}

export interface StudentEvidence {
  id: number;
  student_id: number;
  source: 'RESUME' | 'GITHUB' | 'LINKEDIN' | 'PORTFOLIO' | 'ASSESSMENT' | string;
  source_url?: string;
  evidence_type: string;
  extracted_data?: any;
  created_at: string;
  last_synced_at?: string;
  confidence?: number;
  verification_status: string;
}

export interface TargetCompany {
  id: number;
  name: string;
  normalized_name: string;
  website?: string;
  description?: string;
  active: boolean;
}

export interface CareerRole {
  id: number;
  name: string;
  description?: string;
}

export interface CareerGoal {
  id: number;
  career_role_id: number;
  target_company_id?: number;
  career_role?: CareerRole;
  target_company?: TargetCompany;
}

export const getStudentProfile = async () => {
  const { data } = await apiClient.get('/api/v1/student/profile');
  return data;
};

export const updateStudentProfile = async (profile: StudentProfile) => {
  const { data } = await apiClient.put('/api/v1/student/profile', profile);
  return data;
};

export const updateGemsPreferences = async (prefs: GemsPreferences) => {
  const { data } = await apiClient.post('/api/v1/student/preferences/gems', prefs);
  return data;
};

export const getAcademicProfile = async () => {
  const { data } = await apiClient.get('/api/v1/student/academic');
  return data;
};

export const updateAcademicProfile = async (profile: AcademicProfile) => {
  const { data } = await apiClient.put('/api/v1/student/academic', profile);
  return data;
};

export const getProfessionalProfile = async () => {
  const { data } = await apiClient.get<ProfessionalProfile>('/api/v1/student/professional');
  return data;
};

export const updateProfessionalProfile = async (profile: ProfessionalProfile) => {
  const { data } = await apiClient.put<ProfessionalProfile>('/api/v1/student/professional', profile);
  return data;
};

export const getExternalProfiles = async () => {
  const { data } = await apiClient.get<ExternalProfiles>('/api/v1/student/external-profiles');
  return data;
};

export const updateExternalProfiles = async (profiles: ExternalProfiles) => {
  const { data } = await apiClient.put<ExternalProfiles>('/api/v1/student/external-profiles', profiles);
  return data;
};

export const syncGitHubProfile = async () => {
  const { data } = await apiClient.post<StudentEvidence>('/api/v1/student/github/sync');
  return data;
};

export const uploadResume = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const { data } = await apiClient.post<StudentResume>('/api/v1/student/resume/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
};

export const getActiveResume = async () => {
  const { data } = await apiClient.get<StudentResume | null>('/api/v1/student/resume/active');
  return data;
};

export const getResumeDownloadUrl = (resumeId: number) => {
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
  return `${baseURL}/api/v1/student/resume/${resumeId}/download`;
};

export const getStudentEvidence = async () => {
  const { data } = await apiClient.get<StudentEvidence[]>('/api/v1/student/evidence');
  return data;
};

export const getCareerRoles = async () => {
  const { data } = await apiClient.get<CareerRole[]>('/api/v1/career-goal/roles');
  return data;
};

export interface TargetCompanyRoleResponse {
  id: number;
  company_id: number;
  career_role_id: number;
  company: TargetCompany;
  career_role: CareerRole;
}

export const getTargetCompanies = async () => {
  const { data } = await apiClient.get<TargetCompany[]>('/api/v1/career-goal/companies');
  return data;
};

export const getTargetCompanyRoles = async (companyId: number) => {
  const { data } = await apiClient.get<TargetCompanyRoleResponse[]>(`/api/v1/career-goal/companies/${companyId}/roles`);
  return data;
};

export const getCareerGoal = async () => {
  const { data } = await apiClient.get<CareerGoal>('/api/v1/career-goal/goal');
  return data;
};


export const updateCareerGoal = async (careerRoleId: number, targetCompanyId?: number | null) => {
  const { data } = await apiClient.put<CareerGoal>('/api/v1/career-goal/goal', {
    career_role_id: careerRoleId,
    target_company_id: targetCompanyId || null,
  });
  return data;
};

