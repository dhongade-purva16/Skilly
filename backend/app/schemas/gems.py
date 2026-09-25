from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import date

class GemsTaskResource(BaseModel):
    resource_id: int
    title: str
    source_url: str
    difficulty: Optional[str] = None
    provider: Optional[str] = None

class GemsTaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: str
    estimated_minutes: int
    priority: str
    scheduled_date: date
    order_index: int
    resource_references: List[GemsTaskResource] = []

class GemsTaskResponse(GemsTaskBase):
    id: int
    daily_plan_id: int
    roadmap_step_id: Optional[int]
    skill_id: Optional[int]
    skill_name: Optional[str] = None
    status: str
    completion_note: Optional[str] = None

    class Config:
        from_attributes = True

class GemsDailyPlanSummary(BaseModel):
    total: int
    completed: int
    in_progress: int
    skipped: int
    remaining: int
    estimated_remaining_minutes: int

class GemsDailyPlanResponse(BaseModel):
    id: int
    plan_date: date
    roadmap_id: Optional[int]
    status: str
    summary: GemsDailyPlanSummary
    tasks: List[GemsTaskResponse] = []

    class Config:
        from_attributes = True

class HelpContextResponse(BaseModel):
    task_id: int
    skill: str
    task: str
    help_available: bool
    resources: List[GemsTaskResource] = []
