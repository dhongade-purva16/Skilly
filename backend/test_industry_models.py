import pytest
import uuid
from app.core.database import SessionLocal
from app.models import (
    User, TargetCompany, HRProfile, CompanyJob, CompanyJobSkill,
    SkillCategory, Skill, JobApplication, Student, Assessment,
    AssessmentQuestion, AssessmentAttempt
)

def test_industry_models():
    db = SessionLocal()
    
    unique_suffix = str(uuid.uuid4())[:8]
    
    try:
        # Create Company
        company = TargetCompany(name=f"Test Corp {unique_suffix}", normalized_name=f"test_corp_{unique_suffix}")
        db.add(company)
        db.commit()

        # Create HR User
        user = User(firebase_uid=f"test_hr_uid_{unique_suffix}", email=f"hr_{unique_suffix}@testcorp.com", user_type="hr")
        db.add(user)
        db.commit()

        # Create HRProfile
        hr_profile = HRProfile(user_id=user.id, company_id=company.id)
        db.add(hr_profile)
        db.commit()

        # Create CompanyJob
        job = CompanyJob(company_id=company.id, title=f"Test Job {unique_suffix}", description="Test Desc")
        db.add(job)
        db.commit()

        # Create Skill Categories and Skills
        cat_tech = SkillCategory(name=f"Technical {unique_suffix}")
        cat_soft = SkillCategory(name=f"Soft Skills {unique_suffix}")
        db.add_all([cat_tech, cat_soft])
        db.commit()

        skill_tech = Skill(name=f"Python {unique_suffix}", category_id=cat_tech.id)
        skill_soft = Skill(name=f"Communication {unique_suffix}", category_id=cat_soft.id)
        db.add_all([skill_tech, skill_soft])
        db.commit()

        # Map Skills to Job
        js1 = CompanyJobSkill(job_id=job.id, skill_id=skill_tech.id, required_level=3)
        js2 = CompanyJobSkill(job_id=job.id, skill_id=skill_soft.id, required_level=4)
        db.add_all([js1, js2])
        db.commit()

        # Create Student
        student_user = User(firebase_uid=f"student_uid_{unique_suffix}", email=f"student_{unique_suffix}@test.com")
        db.add(student_user)
        db.commit()
        
        student = Student(user_id=student_user.id)
        db.add(student)
        db.commit()

        # Job Application
        app = JobApplication(job_id=job.id, student_id=student.id, status="applied")
        db.add(app)
        db.commit()

        # Assessment Linkage
        assessment = Assessment(title=f"Test Assessment {unique_suffix}", company_job_id=job.id, total_marks=100)
        db.add(assessment)
        db.commit()

        # Questions
        q1 = AssessmentQuestion(assessment_id=assessment.id, question_text="Python?", skill_id=skill_tech.id, options=["A", "B"], correct_option_index=0)
        q2 = AssessmentQuestion(assessment_id=assessment.id, question_text="Comm?", skill_id=skill_soft.id, options=["A", "B"], correct_option_index=0)
        db.add_all([q1, q2])
        db.commit()

        # Assessment Attempt
        attempt = AssessmentAttempt(student_id=student.id, assessment_id=assessment.id, overall_score=80.0, skill_wise_scores={"Python": 100, "Communication": 60})
        db.add(attempt)
        db.commit()
        
        app.assessment_attempt_id = attempt.id
        db.commit()

        # Assertions
        assert hr_profile.id is not None
        assert job.id is not None
        assert len(job.skills) == 2
        assert app.id is not None
        assert assessment.id is not None
        assert attempt.overall_score == 80.0
        assert attempt.skill_wise_scores["Python"] == 100

        print("All industry model tests passed.")
    finally:
        # Cleanup properly resolving potential FK issues
        db.rollback()
        db.query(JobApplication).filter_by(job_id=job.id).delete()
        db.query(AssessmentAttempt).filter_by(assessment_id=assessment.id).delete()
        db.query(AssessmentQuestion).filter_by(assessment_id=assessment.id).delete()
        db.query(Assessment).filter_by(id=assessment.id).delete()
        db.query(CompanyJobSkill).filter_by(job_id=job.id).delete()
        db.query(CompanyJob).filter_by(id=job.id).delete()
        db.query(HRProfile).filter_by(id=hr_profile.id).delete()
        db.query(Student).filter_by(id=student.id).delete()
        db.query(User).filter(User.id.in_([user.id, student_user.id])).delete()
        db.query(Skill).filter(Skill.id.in_([skill_tech.id, skill_soft.id])).delete()
        db.query(SkillCategory).filter(SkillCategory.id.in_([cat_tech.id, cat_soft.id])).delete()
        db.query(TargetCompany).filter_by(id=company.id).delete()
        db.commit()
        db.close()
