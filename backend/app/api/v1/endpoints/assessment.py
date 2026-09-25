from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from app.api import deps
from app.models import (
    User, Assessment, AssessmentQuestion, AssessmentAttempt, AssessmentAnswer,
    StudentSkill, SkillEvidence, StudentEvidence, TargetCompany
)
from app.schemas.assessment import (
    AssessmentResponse, AssessmentDetailResponse, AssessmentSubmission, AssessmentResultResponse
)

router = APIRouter()

@router.get("/", response_model=List[AssessmentResponse])
def list_assessments(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    assessments = db.query(Assessment).all()
    result = []
    for a in assessments:
        res = AssessmentResponse.model_validate(a)
        if a.target_company_id:
            res.assessment_source = "company_specific"
            res.target_company_name = a.target_company.name if a.target_company else None
        else:
            res.assessment_source = "role_fallback"
            res.target_company_name = None
        result.append(res)
    return result

@router.get("/{assessment_id}", response_model=AssessmentDetailResponse)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    res = AssessmentDetailResponse.model_validate(assessment)
    if assessment.target_company_id:
        res.assessment_source = "company_specific"
        res.target_company_name = assessment.target_company.name if assessment.target_company else None
    else:
        res.assessment_source = "role_fallback"
        res.target_company_name = None
    return res

@router.post("/{assessment_id}/attempt", response_model=AssessmentResultResponse)
def start_attempt(
    assessment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    student = current_user.student
    if not student:
        raise HTTPException(status_code=400, detail="Student profile not found")

    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    attempt = AssessmentAttempt(
        student_id=student.id,
        assessment_id=assessment_id,
        started_at=datetime.now(timezone.utc)
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

@router.post("/attempt/{attempt_id}/submit", response_model=AssessmentResultResponse)
def submit_attempt(
    attempt_id: int,
    submission: AssessmentSubmission,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    student = current_user.student
    if not student:
        raise HTTPException(status_code=400, detail="Student profile not found")
        
    attempt = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.id == attempt_id, 
        AssessmentAttempt.student_id == student.id
    ).first()
    
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.completed_at:
        raise HTTPException(status_code=400, detail="Attempt already submitted")

    # Evaluate
    correct_count = 0
    total_questions = len(attempt.assessment.questions)
    
    question_dict = {q.id: q for q in attempt.assessment.questions}
    
    for ans in submission.answers:
        q = question_dict.get(ans.question_id)
        if q:
            is_correct = ans.selected_option_index == q.correct_option_index
            if is_correct:
                correct_count += 1
            
            db_answer = AssessmentAnswer(
                attempt_id=attempt.id,
                question_id=q.id,
                selected_option_index=ans.selected_option_index,
                is_correct=is_correct
            )
            db.add(db_answer)

    score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0.0
    
    attempt.score = score_percentage
    attempt.completed_at = datetime.now(timezone.utc)
    
    # Update Student Skill
    skill_id = attempt.assessment.skill_id
    student_skill = db.query(StudentSkill).filter(
        StudentSkill.student_id == student.id, 
        StudentSkill.skill_id == skill_id
    ).first()
    
    new_proficiency = min(5, max(1, int(score_percentage // 20) + 1))
    if score_percentage == 0:
        new_proficiency = 0
    
    if not student_skill:
        student_skill = StudentSkill(
            student_id=student.id,
            skill_id=skill_id,
            proficiency_level=new_proficiency,
            score=score_percentage,
            confidence=0.8,
            last_assessed_at=datetime.now(timezone.utc)
        )
        db.add(student_skill)
    else:
        student_skill.score = score_percentage
        student_skill.proficiency_level = new_proficiency
        student_skill.last_assessed_at = datetime.now(timezone.utc)
        
    # Create skill evidence
    evidence = SkillEvidence(
        student_id=student.id,
        skill_id=skill_id,
        source_type="Assessment",
        source_id=attempt.id,
        evidence_score=score_percentage
    )
    db.add(evidence)
    
    # Generic Student Evidence layer record (Requirement 3)
    gen_evidence = StudentEvidence(
        student_id=student.id,
        source="ASSESSMENT",
        evidence_type="ASSESSMENT_COMPLETED",
        extracted_data={
            "assessment_id": attempt.assessment_id,
            "assessment_title": attempt.assessment.title,
            "score": score_percentage,
            "attempt_id": attempt.id
        },
        created_at=datetime.now(timezone.utc),
        confidence=0.9,
        verification_status="verified"
    )
    db.add(gen_evidence)

    db.commit()
    db.refresh(attempt)
    return attempt

