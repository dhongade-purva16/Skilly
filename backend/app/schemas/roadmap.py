from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime

class RoadmapTarget(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None

class RoadmapResource(BaseModel):
    resource_id: int
    title: str
    source_url: str
    difficulty: Optional[str] = None
    provider: Optional[str] = None

class RoadmapStepBase(BaseModel):
    step_order: int
    skill_id: int
    skill_name: str
    priority: str
    objective: str
    description: Optional[str] = None
    estimated_duration: Optional[str] = None
    resources: List[RoadmapResource] = []
    practice_task: Optional[str] = None
    status: str = "not_started"

class RoadmapStepResponse(RoadmapStepBase):
    id: int
    roadmap_id: int

    class Config:
        from_attributes = True

class RoadmapResponse(BaseModel):
    roadmap_id: int
    target: RoadmapTarget
    summary: Optional[str] = None
    status: str = "not_started"
    steps: List[RoadmapStepResponse] = []

    class Config:
        from_attributes = True
