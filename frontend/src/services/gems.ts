import apiClient from './apiClient';

export interface GemsTaskResource {
  resource_id: number;
  title: string;
  source_url: string;
  difficulty?: string;
  provider?: string;
}

export interface GemsTask {
  id: number;
  daily_plan_id: number;
  roadmap_step_id?: number;
  skill_id?: number;
  skill_name?: string;
  title: string;
  description?: string;
  task_type: string;
  estimated_minutes: number;
  priority: string;
  scheduled_date: string;
  status: string;
  order_index: number;
  resource_references: GemsTaskResource[];
  completion_note?: string;
}

export interface GemsDailyPlanSummary {
  total: number;
  completed: number;
  in_progress: number;
  skipped: number;
  remaining: number;
  estimated_remaining_minutes: number;
}

export interface GemsDailyPlanResponse {
  id: number;
  plan_date: string;
  roadmap_id?: number;
  status: string;
  summary: GemsDailyPlanSummary;
  tasks: GemsTask[];
}

export interface HelpContextResponse {
  task_id: number;
  skill: string;
  task: string;
  help_available: boolean;
  resources: GemsTaskResource[];
}

export const getDailyPlan = async (): Promise<GemsDailyPlanResponse | null> => {
  try {
    const response = await apiClient.get<GemsDailyPlanResponse>('/api/v1/student/gems/today');
    return response.data;
  } catch (error: any) {
    if (error.response && error.response.status === 404) {
      return null;
    }
    throw error;
  }
};

export const startGemsTask = async (taskId: number): Promise<GemsTask> => {
  const response = await apiClient.post<GemsTask>(`/api/v1/student/gems/tasks/${taskId}/start`);
  return response.data;
};

export const completeGemsTask = async (taskId: number, note?: string): Promise<GemsTask> => {
  const response = await apiClient.post<GemsTask>(`/api/v1/student/gems/tasks/${taskId}/complete`, { note });
  return response.data;
};

export const skipGemsTask = async (taskId: number, reason?: string): Promise<GemsTask> => {
  const response = await apiClient.post<GemsTask>(`/api/v1/student/gems/tasks/${taskId}/skip`, { note: reason });
  return response.data;
};

export const rescheduleGemsTask = async (taskId: number): Promise<GemsTask> => {
  const response = await apiClient.post<GemsTask>(`/api/v1/student/gems/tasks/${taskId}/reschedule`);
  return response.data;
};

export const getGemsTaskHelp = async (taskId: number): Promise<HelpContextResponse> => {
  const response = await apiClient.get<HelpContextResponse>(`/api/v1/student/gems/tasks/${taskId}/help`);
  return response.data;
};
