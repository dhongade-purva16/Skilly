from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.api import deps
from app.models import (
    User, CompanyJob, JobApplication, Assessment, AssessmentAttempt,
    AssessmentQuestion, AssessmentAnswer
)
from app.schemas.industry import (
    CompanyJobResponse, JobApplicationResponse, AssessmentResponse,
    AssessmentAttemptResponse, AssessmentSubmission
)

router = APIRouter()

@router.get("/jobs", response_model=List[CompanyJobResponse])
def get_available_jobs(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student_user)
):
    # Retrieve all active jobs
    jobs = db.query(CompanyJob).filter(CompanyJob.status == "active").all()
    return jobs

@router.get("/jobs/{job_id}", response_model=CompanyJobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student_user)
):
    job = db.query(CompanyJob).filter(CompanyJob.id == job_id, CompanyJob.status == "active").first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/jobs/{job_id}/apply", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
def apply_for_job(
    job_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student_user)
):
    student_id = current_user.student.id
    
    job = db.query(CompanyJob).filter(CompanyJob.id == job_id, CompanyJob.status == "active").first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not available")
        
    if job.deadline and job.deadline < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Job application deadline has passed")
        
    initial_status = "assessment_pending" if job.assessment_required else "applied"
    
    app = JobApplication(
        job_id=job.id,
        student_id=student_id,
        status=initial_status
    )
    
    try:
        db.add(app)
        db.commit()
        db.refresh(app)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Already applied to this job")
        
    return app

@router.get("/applications", response_model=List[JobApplicationResponse])
def get_applications(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student_user)
):
    apps = db.query(JobApplication).filter(JobApplication.student_id == current_user.student.id).all()
    return apps

@router.get("/applications/{application_id}/assessment", response_model=AssessmentResponse)
def get_application_assessment(
    application_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student_user)
):
    app = db.query(JobApplication).filter(
        JobApplication.id == application_id,
        JobApplication.student_id == current_user.student.id
    ).first()
    
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    assessment = db.query(Assessment).filter(Assessment.company_job_id == app.job_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found for this job")
        
    # Exclude correct options from response by modifying the objects or using a tailored Pydantic schema
    # (The AssessmentQuestionResponse schema already defines correct_option_index as Optional,
    # but to completely hide it, we could set it to None here before returning)
    for q in assessment.questions:
        q.correct_option_index = None
        
    return assessment

@router.post("/applications/{application_id}/assessment/start", response_model=AssessmentAttemptResponse)
def start_assessment(
    application_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student_user)
):
    app = db.query(JobApplication).filter(
        JobApplication.id == application_id,
        JobApplication.student_id == current_user.student.id
    ).first()
    
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    if app.status != "assessment_pending":
        raise HTTPException(status_code=400, detail="Assessment is not pending for this application")
        
    assessment = db.query(Assessment).filter(Assessment.company_job_id == app.job_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    # Check if attempt already exists
    if app.assessment_attempt_id:
        attempt = db.query(AssessmentAttempt).filter(AssessmentAttempt.id == app.assessment_attempt_id).first()
        return attempt
        
    attempt = AssessmentAttempt(
        student_id=current_user.student.id,
        assessment_id=assessment.id
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    app.assessment_attempt_id = attempt.id
    db.commit()
    
    return attempt

@router.post("/assessments/{attempt_id}/submit", response_model=AssessmentAttemptResponse)
def submit_assessment(
    attempt_id: int,
    submission: AssessmentSubmission,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student_user)
):
    attempt = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.id == attempt_id,
        AssessmentAttempt.student_id == current_user.student.id
    ).first()
    
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
        
    if attempt.completed_at:
        raise HTTPException(status_code=400, detail="Assessment already submitted")
        
    assessment = db.query(Assessment).filter(Assessment.id == attempt.assessment_id).first()
    
    # Calculate score
    total_score = 0
    skill_scores = {} # skill_id -> {correct: X, total: Y}
    
    for question in assessment.questions:
        if question.skill_id:
            if question.skill.name not in skill_scores:
                skill_scores[question.skill.name] = {"correct": 0, "total": 0}
            skill_scores[question.skill.name]["total"] += 1
            
        selected_idx = submission.answers.get(question.id)
        is_correct = (selected_idx == question.correct_option_index)
        
        if is_correct:
            total_score += 1
            if question.skill_id:
                skill_scores[question.skill.name]["correct"] += 1
                
        ans = AssessmentAnswer(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_option_index=selected_idx,
            is_correct=is_correct
        )
        db.add(ans)
        
    # Finalize skill-wise percentages
    final_skill_scores = {}
    for skill_name, stats in skill_scores.items():
        if stats["total"] > 0:
            final_skill_scores[skill_name] = (stats["correct"] / stats["total"]) * 100
            
    overall_percentage = (total_score / len(assessment.questions)) * 100 if assessment.questions else 0
    
    attempt.overall_score = overall_percentage
    attempt.skill_wise_scores = final_skill_scores
    attempt.completed_at = datetime.now(timezone.utc)
    db.commit()
    
    # Update JobApplication
    app = db.query(JobApplication).filter(JobApplication.assessment_attempt_id == attempt.id).first()
    if app:
        app.status = "assessment_completed"
        db.commit()
        
    db.refresh(attempt)
    return attempt
