from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.api import deps
from app.models import (
    User, CompanyJob, CompanyJobSkill, JobApplication, Assessment, 
    AssessmentQuestion, Skill
)
from app.schemas.industry import (
    CompanyJobCreate, CompanyJobUpdate, CompanyJobResponse,
    JobApplicationResponse, AssessmentCreate, AssessmentResponse, AssessmentUpdate
)

router = APIRouter()

@router.post("/jobs", response_model=CompanyJobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job_in: CompanyJobCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_hr_user)
):
    company_id = current_user.hr_profile.company_id
    
    # Create Job
    job = CompanyJob(
        company_id=company_id,
        title=job_in.title,
        description=job_in.description,
        location=job_in.location,
        work_mode=job_in.work_mode,
        eligibility=job_in.eligibility,
        experience_requirement=job_in.experience_requirement,
        deadline=job_in.deadline,
        assessment_required=job_in.assessment_required
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Attach Skills
    for skill_in in job_in.skills:
        # Validate skill existence
        skill = db.query(Skill).filter(Skill.id == skill_in.skill_id).first()
        if not skill:
            continue
        
        job_skill = CompanyJobSkill(
            job_id=job.id,
            skill_id=skill.id,
            required_level=skill_in.required_level,
            priority=skill_in.priority
        )
        db.add(job_skill)
    db.commit()
    db.refresh(job)
    return job

@router.get("/jobs", response_model=List[CompanyJobResponse])
def get_jobs(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_hr_user)
):
    company_id = current_user.hr_profile.company_id
    jobs = db.query(CompanyJob).filter(CompanyJob.company_id == company_id).all()
    return jobs

@router.get("/jobs/{job_id}", response_model=CompanyJobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_hr_user)
):
    company_id = current_user.hr_profile.company_id
    job = db.query(CompanyJob).filter(CompanyJob.id == job_id, CompanyJob.company_id == company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/jobs/{job_id}", response_model=CompanyJobResponse)
def update_job(
    job_id: int,
    job_in: CompanyJobUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_hr_user)
):
    company_id = current_user.hr_profile.company_id
    job = db.query(CompanyJob).filter(CompanyJob.id == job_id, CompanyJob.company_id == company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_data = job_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)
    
    db.commit()
    db.refresh(job)
    return job

@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_hr_user)
):
    company_id = current_user.hr_profile.company_id
    job = db.query(CompanyJob).filter(CompanyJob.id == job_id, CompanyJob.company_id == company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()
    return None

@router.get("/jobs/{job_id}/applications", response_model=List[JobApplicationResponse])
def get_job_applications(
    job_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_hr_user)
):
    company_id = current_user.hr_profile.company_id
    job = db.query(CompanyJob).filter(CompanyJob.id == job_id, CompanyJob.company_id == company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    apps = db.query(JobApplication).filter(JobApplication.job_id == job_id).all()
    return apps

@router.post("/applications/{application_id}/shortlist", response_model=JobApplicationResponse)
def shortlist_application(
    application_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_hr_user)
):
    company_id = current_user.hr_profile.company_id
    
    app = db.query(JobApplication).join(CompanyJob).filter(
        JobApplication.id == application_id,
        CompanyJob.company_id == company_id
    ).first()
    
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if app.company_job.assessment_required and app.status != "assessment_completed":
        raise HTTPException(status_code=400, detail="Assessment must be completed before shortlisting")
    
    app.status = "shortlisted"
    db.commit()
    db.refresh(app)
    return app

@router.post("/jobs/{job_id}/assessment", response_model=AssessmentResponse)
def create_assessment(
    job_id: int,
    assessment_in: AssessmentCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_hr_user)
):
    company_id = current_user.hr_profile.company_id
    job = db.query(CompanyJob).filter(CompanyJob.id == job_id, CompanyJob.company_id == company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    assessment = Assessment(
        title=assessment_in.title,
        description=assessment_in.description,
        total_marks=assessment_in.total_marks,
        passing_criteria=assessment_in.passing_criteria,
        company_job_id=job.id,
        target_company_id=company_id
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    for q_in in assessment_in.questions:
        q = AssessmentQuestion(
            assessment_id=assessment.id,
            question_text=q_in.question_text,
            options=q_in.options,
            correct_option_index=q_in.correct_option_index,
            difficulty=q_in.difficulty,
            skill_id=q_in.skill_id
        )
        db.add(q)
    db.commit()
    db.refresh(assessment)
    return assessment

@router.get("/jobs/{job_id}/assessment", response_model=AssessmentResponse)
def get_assessment(
    job_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_hr_user)
):
    company_id = current_user.hr_profile.company_id
    job = db.query(CompanyJob).filter(CompanyJob.id == job_id, CompanyJob.company_id == company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    assessment = db.query(Assessment).filter(Assessment.company_job_id == job.id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment
