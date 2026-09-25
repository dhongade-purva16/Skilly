import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.main import app
from app.core.database import SessionLocal
from app.api import deps
from app.models import User, TargetCompany, HRProfile, Student, Skill, SkillCategory

client = TestClient(app)

# Global test data
TEST_SUFFIX = str(uuid.uuid4())[:8]

def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[deps.get_db] = get_test_db

from fastapi import Depends

def get_hr_user(db: Session = Depends(get_test_db)):
    user = db.query(User).filter(User.user_type == "hr").first()
    return user

def get_student_user(db: Session = Depends(get_test_db)):
    user = db.query(User).filter(User.user_type == "student").first()
    return user


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    db = SessionLocal()
    # Create test data
    company = TargetCompany(name=f"API Test Corp {TEST_SUFFIX}", normalized_name=f"api_corp_{TEST_SUFFIX}")
    db.add(company)
    db.commit()

    hr_user = User(firebase_uid=f"hr_{TEST_SUFFIX}", email=f"hr_{TEST_SUFFIX}@test.com", user_type="hr")
    db.add(hr_user)
    db.commit()

    hr_profile = HRProfile(user_id=hr_user.id, company_id=company.id)
    db.add(hr_profile)
    db.commit()

    student_user = User(firebase_uid=f"student_{TEST_SUFFIX}", email=f"student_{TEST_SUFFIX}@test.com", user_type="student")
    db.add(student_user)
    db.commit()

    student = Student(user_id=student_user.id)
    db.add(student)
    db.commit()
    
    cat_tech = SkillCategory(name=f"Tech {TEST_SUFFIX}")
    db.add(cat_tech)
    db.commit()
    
    skill = Skill(name=f"Python {TEST_SUFFIX}", category_id=cat_tech.id)
    db.add(skill)
    db.commit()

    yield
    
    # Cleanup will be handled manually to avoid FK issues with other tests, but since it's a test db...
    db.close()

def test_hr_create_job():
    app.dependency_overrides[deps.get_current_hr_user] = get_hr_user
    with SessionLocal() as db:
        skill = db.query(Skill).filter(Skill.name == f"Python {TEST_SUFFIX}").first()

        payload = {
            "title": "Software Engineer",
            "description": "Develop stuff",
            "assessment_required": True,
            "skills": [
                {
                    "skill_id": skill.id,
                    "required_level": 3,
                    "priority": "HIGH"
                }
            ]
        }
    response = client.post("/api/v1/company/jobs", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Software Engineer"
    assert len(data["skills"]) == 1

def test_student_get_jobs():
    app.dependency_overrides[deps.get_current_student_user] = get_student_user
    response = client.get("/api/v1/student/jobs")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    
def test_student_apply_job():
    app.dependency_overrides[deps.get_current_student_user] = get_student_user
    # Get the job created by HR
    response = client.get("/api/v1/student/jobs")
    jobs = response.json()
    job_id = jobs[-1]["id"]
    
    response = client.post(f"/api/v1/student/jobs/{job_id}/apply")
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "assessment_pending"
    
def test_student_duplicate_apply():
    app.dependency_overrides[deps.get_current_student_user] = get_student_user
    response = client.get("/api/v1/student/jobs")
    job_id = response.json()[-1]["id"]
    
    response = client.post(f"/api/v1/student/jobs/{job_id}/apply")
    assert response.status_code == 409

def test_hr_create_assessment():
    app.dependency_overrides[deps.get_current_hr_user] = get_hr_user
    
    # Get the job
    response = client.get("/api/v1/company/jobs")
    job_id = response.json()[-1]["id"]
    
    with SessionLocal() as db:
        skill = db.query(Skill).filter(Skill.name == f"Python {TEST_SUFFIX}").first()
        
        payload = {
            "title": "Backend Test",
            "total_marks": 100,
            "passing_criteria": 70.0,
            "questions": [
                {
                    "question_text": "What is Python?",
                    "options": ["Snake", "Language", "Car", "None"],
                    "correct_option_index": 1,
                    "skill_id": skill.id
                }
            ]
        }
    
    response = client.post(f"/api/v1/company/jobs/{job_id}/assessment", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Backend Test"
    assert len(data["questions"]) == 1

def test_student_start_and_submit_assessment():
    app.dependency_overrides[deps.get_current_student_user] = get_student_user
    
    response = client.get("/api/v1/student/applications")
    app_id = response.json()[-1]["id"]
    
    # Start
    start_resp = client.post(f"/api/v1/student/applications/{app_id}/assessment/start")
    assert start_resp.status_code == 200
    attempt_id = start_resp.json()["id"]
    
    # Submit correctly
    # Need to know question ID, we fetch assessment
    assessment_resp = client.get(f"/api/v1/student/applications/{app_id}/assessment")
    q_id = assessment_resp.json()["questions"][0]["id"]
    
    submit_payload = {
        "answers": {
            str(q_id): 1
        }
    }
    
    sub_resp = client.post(f"/api/v1/student/assessments/{attempt_id}/submit", json=submit_payload)
    assert sub_resp.status_code == 200
    data = sub_resp.json()
    
    assert data["overall_score"] == 100.0
    assert data["skill_wise_scores"][f"Python {TEST_SUFFIX}"] == 100.0

def test_hr_shortlist_applicant():
    app.dependency_overrides[deps.get_current_hr_user] = get_hr_user
    
    response = client.get("/api/v1/company/jobs")
    job_id = response.json()[-1]["id"]
    
    apps_resp = client.get(f"/api/v1/company/jobs/{job_id}/applications")
    app_id = apps_resp.json()[-1]["id"]
    
    sl_resp = client.post(f"/api/v1/company/applications/{app_id}/shortlist")
    assert sl_resp.status_code == 200
    assert sl_resp.json()["status"] == "shortlisted"
