from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Job Skills
class CompanyJobSkillCreate(BaseModel):
    skill_id: int
    required_level: int = 1
    priority: str = "MEDIUM"

class CompanyJobSkillResponse(BaseModel):
    id: int
    skill_id: int
    required_level: int
    priority: str

    class Config:
        from_attributes = True

# Company Job
class CompanyJobCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = None
    eligibility: Optional[str] = None
    experience_requirement: Optional[str] = None
    deadline: Optional[datetime] = None
    assessment_required: bool = True
    skills: List[CompanyJobSkillCreate] = []

class CompanyJobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = None
    eligibility: Optional[str] = None
    experience_requirement: Optional[str] = None
    deadline: Optional[datetime] = None
    assessment_required: Optional[bool] = None
    status: Optional[str] = None

class CompanyJobResponse(BaseModel):
    id: int
    company_id: int
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = None
    eligibility: Optional[str] = None
    experience_requirement: Optional[str] = None
    deadline: Optional[datetime] = None
    assessment_required: bool
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    skills: List[CompanyJobSkillResponse] = []

    class Config:
        from_attributes = True

# Applications
class JobApplicationResponse(BaseModel):
    id: int
    job_id: int
    student_id: int
    status: str
    assessment_attempt_id: Optional[int] = None
    applied_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Assessment
class AssessmentQuestionCreate(BaseModel):
    question_text: str
    options: List[str]
    correct_option_index: int
    difficulty: int = 1
    skill_id: Optional[int] = None

class AssessmentQuestionResponse(BaseModel):
    id: int
    question_text: str
    options: List[str]
    correct_option_index: Optional[int] = None # Should be hidden for students in practice
    difficulty: int
    skill_id: Optional[int] = None

    class Config:
        from_attributes = True

class AssessmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    total_marks: Optional[int] = None
    passing_criteria: Optional[float] = None
    questions: List[AssessmentQuestionCreate] = []

class AssessmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    total_marks: Optional[int] = None
    passing_criteria: Optional[float] = None

class AssessmentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    company_job_id: Optional[int] = None
    total_marks: Optional[int] = None
    passing_criteria: Optional[float] = None
    questions: List[AssessmentQuestionResponse] = []

    class Config:
        from_attributes = True

# Attempts
class AssessmentSubmission(BaseModel):
    # Mapping of question_id -> selected_option_index
    answers: Dict[int, int]

class AssessmentAttemptResponse(BaseModel):
    id: int
    student_id: int
    assessment_id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    overall_score: Optional[float] = None
    skill_wise_scores: Optional[Dict[str, float]] = None

    class Config:
        from_attributes = True
