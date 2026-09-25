from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.skill import SkillResponse

class AchieverStudentContext(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None

class AchieverAcademicContext(BaseModel):
    degree: Optional[str] = None
    branch: Optional[str] = None
    academic_year: Optional[str] = None
    graduation_year: Optional[int] = None

class AchieverProfessionalContext(BaseModel):
    headline: Optional[str] = None
    current_status: Optional[str] = None
    experience_level: Optional[str] = None
    years_of_experience: Optional[float] = None
    professional_summary: Optional[str] = None
    work_domain: Optional[str] = None

class AchieverTargetCompanyRoleContext(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class AchieverTargetContext(BaseModel):
    target_company: Optional[AchieverTargetCompanyRoleContext] = None
    target_role: Optional[AchieverTargetCompanyRoleContext] = None
    career_role: Optional[AchieverTargetCompanyRoleContext] = None

class AchieverExternalProfilesContext(BaseModel):
    github_status: str
    github_url: Optional[str] = None
    linkedin_status: str
    linkedin_url: Optional[str] = None
    portfolio_status: str
    portfolio_url: Optional[str] = None

class AchieverResumeContext(BaseModel):
    filename: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    upload_date: Optional[datetime] = None
    active_status: bool = False
    extraction_status: str
    extracted_text: Optional[str] = None

class AchieverEvidenceContext(BaseModel):
    type: str
    status: str
    title: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AchieverSkillContext(BaseModel):
    skill: SkillResponse
    proficiency_level: int
    source_status: Optional[str] = None
    updated_timestamp: Optional[datetime] = None

class AchieverRequirementContext(BaseModel):
    skill: SkillResponse
    required_proficiency: int
    source: str

class AchieverSkillGapContext(BaseModel):
    skill: SkillResponse
    required_proficiency: int
    current_proficiency: int
    status: str
    requirement_source: str

class AchieverMetadataContext(BaseModel):
    context_version: str
    generated_at: datetime
    requirement_source: str
    available_evidence_count: int
    verified_evidence_count: int
    unverified_evidence_count: int
    has_resume: bool
    has_resume_text: bool
    has_github: bool
    has_linkedin: bool
    has_portfolio: bool
    has_assessment: bool
    has_target_company: bool
    has_target_role: bool

class AchieverContextResponse(BaseModel):
    student: AchieverStudentContext
    academic: AchieverAcademicContext
    professional: AchieverProfessionalContext
    target: AchieverTargetContext
    external_profiles: AchieverExternalProfilesContext
    resume: AchieverResumeContext
    evidence: List[AchieverEvidenceContext]
    skills: List[AchieverSkillContext]
    skill_gaps: List[AchieverSkillGapContext]
    requirements: List[AchieverRequirementContext]
    metadata: AchieverMetadataContext

class EvidenceSummaryItem(BaseModel):
    source: str
    status: str

class PrioritizedSkillGap(BaseModel):
    skill: SkillResponse
    required_proficiency: int
    current_proficiency: int
    gap_status: str
    priority: str
    requirement_source: str
    evidence_summary: List[EvidenceSummaryItem]
    dependency_status: str
    reasons: List[str]

class AchieverPriorityResponse(BaseModel):
    target: AchieverTargetContext
    requirement_source: str
    prioritized_gaps: List[PrioritizedSkillGap]
    summary: str
