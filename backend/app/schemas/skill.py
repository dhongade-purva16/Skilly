from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class SkillCategoryBase(BaseModel):
    name: str

class SkillCategoryResponse(SkillCategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SkillBase(BaseModel):
    name: str
    category_id: int

class SkillResponse(SkillBase):
    id: int
    category: Optional[SkillCategoryResponse] = None
    model_config = ConfigDict(from_attributes=True)

class StudentSkillResponse(BaseModel):
    id: int
    skill_id: int
    proficiency_level: int
    score: float
    confidence: float
    last_assessed_at: Optional[datetime] = None
    skill: SkillResponse
    model_config = ConfigDict(from_attributes=True)

class SkillEvidenceResponse(BaseModel):
    id: int
    skill_id: int
    source_type: str
    source_id: Optional[int]
    evidence_score: float
    created_at: datetime
    skill: SkillResponse
    model_config = ConfigDict(from_attributes=True)
    
class SkillGapResponse(BaseModel):
    skill: SkillResponse
    required_level: int
    current_level: int
    current_score: float
    gap_status: str # "Sufficient", "Gap", "Missing"
    requirement_source: str = "role_fallback" # "company_specific" or "role_fallback"
    target_company_name: Optional[str] = None

