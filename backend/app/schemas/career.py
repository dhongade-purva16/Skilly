from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# Career Role Schemas
class CareerRoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class CareerRoleResponse(CareerRoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Target Company Schemas
class TargetCompanyBase(BaseModel):
    name: str
    normalized_name: str
    website: Optional[str] = None
    description: Optional[str] = None
    active: bool = True

class TargetCompanyResponse(TargetCompanyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TargetCompanyRoleResponse(BaseModel):
    id: int
    company_id: int
    career_role_id: int
    company: TargetCompanyResponse
    career_role: CareerRoleResponse
    model_config = ConfigDict(from_attributes=True)

# Student Career Goal Schemas
class StudentCareerGoalUpdate(BaseModel):
    career_role_id: int
    target_company_id: Optional[int] = None

class StudentCareerGoalResponse(BaseModel):
    id: int
    student_id: int
    career_role_id: int
    target_company_id: Optional[int] = None
    career_role: Optional[CareerRoleResponse] = None
    target_company: Optional[TargetCompanyResponse] = None
    model_config = ConfigDict(from_attributes=True)

