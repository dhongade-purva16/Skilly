from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, List
from datetime import datetime

# Student Schemas
class StudentBase(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    user_id: int
    gems_enabled: bool = False
    gems_reminder_enabled: bool = False
    gems_reminder_time: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class GemsPreferenceUpdate(BaseModel):
    gems_enabled: Optional[bool] = None
    gems_reminder_enabled: Optional[bool] = None
    gems_reminder_time: Optional[str] = None

# Academic Schemas
class AcademicProfileBase(BaseModel):
    degree: Optional[str] = None
    branch: Optional[str] = None
    academic_year: Optional[str] = None
    graduation_year: Optional[int] = None

class AcademicProfileUpdate(AcademicProfileBase):
    pass

class AcademicProfileResponse(AcademicProfileBase):
    id: int
    student_id: int
    model_config = ConfigDict(from_attributes=True)

# Professional Profile Schemas
class ProfessionalProfileBase(BaseModel):
    headline: Optional[str] = None
    current_status: Optional[str] = None
    experience_level: Optional[str] = None
    years_of_experience: Optional[float] = None
    professional_summary: Optional[str] = None
    work_domain: Optional[str] = None

class ProfessionalProfileUpdate(ProfessionalProfileBase):
    pass

class ProfessionalProfileResponse(ProfessionalProfileBase):
    id: int
    student_id: int
    model_config = ConfigDict(from_attributes=True)

# External Profiles Schemas
class ExternalProfilesBase(BaseModel):
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None

class ExternalProfilesUpdate(ExternalProfilesBase):
    pass

class ExternalProfilesResponse(ExternalProfilesBase):
    id: int
    student_id: int
    linkedin_sync_status: str = "Not Synced"
    model_config = ConfigDict(from_attributes=True)

# Resume Schemas
class StudentResumeResponse(BaseModel):
    id: int
    student_id: int
    filename: str
    file_size: int
    content_type: str
    uploaded_at: datetime
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

# Evidence Schemas
class StudentEvidenceResponse(BaseModel):
    id: int
    student_id: int
    source: str # RESUME, GITHUB, LINKEDIN, PORTFOLIO, ASSESSMENT
    source_url: Optional[str] = None
    evidence_type: str
    extracted_data: Optional[Any] = None
    created_at: datetime
    last_synced_at: Optional[datetime] = None
    confidence: Optional[float] = None
    verification_status: str
    model_config = ConfigDict(from_attributes=True)


class GemsPreferenceUpdate(BaseModel):
    gems_enabled: bool
    gems_reminder_enabled: bool = False
    gems_reminder_time: Optional[str] = None

