from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api import deps
from app.models import User, Student, CareerRole, TargetCompany, TargetCompanyRole, StudentCareerGoal
from app.schemas.career import (
    CareerRoleResponse, 
    TargetCompanyResponse, 
    TargetCompanyRoleResponse,
    StudentCareerGoalUpdate, 
    StudentCareerGoalResponse
)

router = APIRouter()

@router.get("/roles", response_model=List[CareerRoleResponse])
def get_career_roles(db: Session = Depends(deps.get_db)):
    """Get all canonical career roles"""
    roles = db.query(CareerRole).all()
    return roles

@router.get("/companies", response_model=List[TargetCompanyResponse])
def get_target_companies(db: Session = Depends(deps.get_db)):
    """Get all canonical target companies"""
    companies = db.query(TargetCompany).filter(TargetCompany.active == True).all()
    return companies

@router.get("/companies/{company_id}/roles", response_model=List[TargetCompanyRoleResponse])
def get_target_company_roles(company_id: int, db: Session = Depends(deps.get_db)):
    """Get career roles associated with a target company"""
    roles = db.query(TargetCompanyRole).filter(TargetCompanyRole.company_id == company_id).all()
    return roles

@router.get("/goal", response_model=StudentCareerGoalResponse)
def get_career_goal(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = current_user.student
    if not student:
        raise HTTPException(status_code=400, detail="Student profile not found")
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.student_id == student.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Career goal not set")
    return goal

@router.put("/goal", response_model=StudentCareerGoalResponse)
def update_career_goal(
    goal_in: StudentCareerGoalUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = current_user.student
    if not student:
        raise HTTPException(status_code=400, detail="Student profile not found")
        
    role = db.query(CareerRole).filter(CareerRole.id == goal_in.career_role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Career role not found")

    target_company = None
    if goal_in.target_company_id:
        target_company = db.query(TargetCompany).filter(TargetCompany.id == goal_in.target_company_id).first()
        if not target_company:
            raise HTTPException(status_code=404, detail="Target company not found")

    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.student_id == student.id).first()
    if not goal:
        goal = StudentCareerGoal(
            student_id=student.id, 
            career_role_id=role.id,
            target_company_id=target_company.id if target_company else None
        )
        db.add(goal)
    else:
        goal.career_role_id = role.id
        goal.target_company_id = target_company.id if target_company else None
        
    db.commit()
    db.refresh(goal)
    return goal


