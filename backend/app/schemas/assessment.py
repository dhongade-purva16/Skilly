from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from datetime import datetime
from .skill import SkillResponse

class AssessmentQuestionBase(BaseModel):
    question_text: str
    options: Any
    difficulty: int

class AssessmentQuestionResponse(AssessmentQuestionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class AssessmentBase(BaseModel):
    title: str
    description: Optional[str]
    skill_id: int

class AssessmentResponse(AssessmentBase):
    id: int
    skill: SkillResponse
    target_company_id: Optional[int] = None
    assessment_source: str = "role_fallback" # "company_specific" or "role_fallback"
    target_company_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class AssessmentDetailResponse(AssessmentResponse):
    questions: List[AssessmentQuestionResponse]
    model_config = ConfigDict(from_attributes=True)

class AssessmentAnswerCreate(BaseModel):
    question_id: int
    selected_option_index: int

class AssessmentSubmission(BaseModel):
    answers: List[AssessmentAnswerCreate]

class AssessmentResultResponse(BaseModel):
    id: int
    assessment_id: int
    score: Optional[float] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
