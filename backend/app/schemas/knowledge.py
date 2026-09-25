from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class KnowledgeResourceResponse(BaseModel):
    resource_id: int
    title: str
    resource_type: str
    provider: str
    difficulty: Optional[str] = None
    source_url: str
    estimated_duration: Optional[str] = None
    similarity_score: float = 0.0

    model_config = ConfigDict(from_attributes=True)

class SkillResourceGroup(BaseModel):
    skill_id: int
    skill_name: str
    priority: str
    resources: List[KnowledgeResourceResponse]

class AchieverResourcesResponse(BaseModel):
    student_id: int
    target: dict
    resources: List[SkillResourceGroup]
