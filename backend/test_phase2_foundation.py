import os
import sys
import unittest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base
from app.api.deps import get_db, get_current_user
from app.models import (
    User, Student, CareerRole, Skill, SkillCategory, CareerRoleSkill,
    TargetCompany, TargetCompanyRole, TargetCompanyRoleSkill,
    StudentCareerGoal, StudentExternalProfiles, StudentResume, StudentEvidence,
    StudentSkill, Assessment, AssessmentQuestion, AssessmentAttempt
)

from app.api.deps import get_current_user

# Setup Test Database or mock dependency override
client = TestClient(app)

# Create test user dependency override
def override_get_current_user():
    db = next(get_db())
    user = db.query(User).filter(User.email == "test_student@example.com").first()
    if not user:
        user = User(firebase_uid="test_firebase_uid_123", email="test_student@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

app.dependency_overrides[get_current_user] = override_get_current_user

class TestPhase2Foundation(unittest.TestCase):

    def setUp(self):
        # Ensure seed data exists
        from seed import seed_db
        seed_db()

    def test_01_external_profiles_linkedin_not_synced(self):
        """Test Requirement 1 & 6: StudentExternalProfiles focused on profile URLs.
        LinkedIn stored as profile URL, not scraped, showing status 'Not Synced'."""
        response = client.put("/api/v1/student/external-profiles", json={
            "github_url": "https://github.com/octocat",
            "linkedin_url": "https://linkedin.com/in/octocat",
            "portfolio_url": "https://octocat.dev"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["github_url"], "https://github.com/octocat")
        self.assertEqual(data["linkedin_url"], "https://linkedin.com/in/octocat")
        self.assertEqual(data["portfolio_url"], "https://octocat.dev")
        self.assertEqual(data["linkedin_sync_status"], "Not Synced")

        # Verify LinkedIn evidence record
        ev_resp = client.get("/api/v1/student/evidence")
        self.assertEqual(ev_resp.status_code, 200)
        evidence = ev_resp.json()
        linkedin_ev = next((e for e in evidence if e["source"] == "LINKEDIN"), None)
        self.assertIsNotNone(linkedin_ev)
        self.assertEqual(linkedin_ev["verification_status"], "not_synced")
        self.assertEqual(linkedin_ev["extracted_data"]["sync_status"], "Not Synced")

    def test_02_resume_private_storage_and_metadata(self):
        """Test Requirement 2 & 5: Resume uses private storage + PostgreSQL metadata.
        Authenticated download works. Evidence created with unverified status."""
        # Create a dummy resume text file
        file_content = b"Resume content for Octocat Developer..."
        response = client.post(
            "/api/v1/student/resume/upload",
            files={"file": ("octocat_resume.pdf", file_content, "application/pdf")}
        )
        self.assertEqual(response.status_code, 200)
        resume_data = response.json()
        self.assertEqual(resume_data["filename"], "octocat_resume.pdf")
        self.assertTrue(resume_data["is_active"])
        resume_id = resume_data["id"]

        # Check authenticated download
        dl_resp = client.get(f"/api/v1/student/resume/{resume_id}/download")
        self.assertEqual(dl_resp.status_code, 200)
        self.assertEqual(dl_resp.content, file_content)

        # Verify resume evidence record (Requirement 3: Evidence does not auto-become verified skill)
        ev_resp = client.get("/api/v1/student/evidence")
        evidence = ev_resp.json()
        resume_ev = next((e for e in evidence if e["source"] == "RESUME"), None)
        self.assertIsNotNone(resume_ev)
        self.assertEqual(resume_ev["verification_status"], "unverified")

    def test_03_github_sync(self):
        """Test Requirement 7: GitHub API synchronization allowed.
        Stores fetched repo info as evidence. Does not automatically assign verified skill levels."""
        client.put("/api/v1/student/external-profiles", json={
            "github_url": "https://github.com/octocat"
        })

        skills_before = client.get("/api/v1/student/skills").json()
        skills_before_dict = {s["skill_id"]: s["proficiency_level"] for s in skills_before}

        sync_resp = client.post("/api/v1/student/github/sync")
        self.assertIn(sync_resp.status_code, [200, 502])
        if sync_resp.status_code == 200:
            ev_data = sync_resp.json()
            self.assertEqual(ev_data["source"], "GITHUB")
            self.assertEqual(ev_data["verification_status"], "unverified")
            self.assertIn("repos", ev_data["extracted_data"])

            # Verify StudentSkills were NOT altered by GitHub sync
            skills_after = client.get("/api/v1/student/skills").json()
            skills_after_dict = {s["skill_id"]: s["proficiency_level"] for s in skills_after}
            self.assertEqual(skills_before_dict, skills_after_dict)


    def test_04_target_company_and_role_fallback(self):
        """Test Requirement 4 & 8: Target company/role career objective.
        Company specific vs role fallback skill gaps."""
        # Get backend role and google company
        roles = client.get("/api/v1/career-goal/roles").json()
        companies = client.get("/api/v1/career-goal/companies").json()
        
        backend_role = next(r for r in roles if r["name"] == "Backend Developer")
        google_company = next(c for c in companies if c["name"] == "Google")
        tcs_company = next(c for c in companies if c["name"] == "TCS")

        # 1. Test Goal with Google (Company Specific)
        client.put("/api/v1/career-goal/goal", json={
            "career_role_id": backend_role["id"],
            "target_company_id": google_company["id"]
        })

        gaps_resp = client.get("/api/v1/student/skill-gaps")
        self.assertEqual(gaps_resp.status_code, 200)
        gaps = gaps_resp.json()
        self.assertTrue(len(gaps) > 0)
        first_gap = gaps[0]
        self.assertEqual(first_gap["requirement_source"], "company_specific")
        self.assertEqual(first_gap["target_company_name"], "Google")

        # 2. Test Goal with TCS (No company-specific skills -> Fallback to Role)
        client.put("/api/v1/career-goal/goal", json={
            "career_role_id": backend_role["id"],
            "target_company_id": tcs_company["id"]
        })

        gaps_resp_fallback = client.get("/api/v1/student/skill-gaps")
        self.assertEqual(gaps_resp_fallback.status_code, 200)
        gaps_fb = gaps_resp_fallback.json()
        self.assertTrue(len(gaps_fb) > 0)
        first_gap_fb = gaps_fb[0]
        self.assertEqual(first_gap_fb["requirement_source"], "role_fallback")

    def test_05_assessment_source_and_evidence(self):
        """Test Requirement 8: Clearly distinguish role-based assessment from company-specific assessment.
        Submission creates verified assessment evidence."""
        assessments_resp = client.get("/api/v1/assessments/")
        self.assertEqual(assessments_resp.status_code, 200)
        assessments = assessments_resp.json()
        self.assertTrue(len(assessments) >= 2)

        role_assessment = next(a for a in assessments if a["assessment_source"] == "role_fallback")
        company_assessment = next(a for a in assessments if a["assessment_source"] == "company_specific")

        self.assertIsNotNone(role_assessment)
        self.assertIsNotNone(company_assessment)
        self.assertEqual(company_assessment["target_company_name"], "Google")

        # Take and submit role assessment
        attempt_start = client.post(f"/api/v1/assessments/{role_assessment['id']}/attempt")
        self.assertEqual(attempt_start.status_code, 200)
        attempt_id = attempt_start.json()["id"]

        detail_resp = client.get(f"/api/v1/assessments/{role_assessment['id']}")
        q_id = detail_resp.json()["questions"][0]["id"]
        correct_idx = detail_resp.json()["questions"][0]["options"].index("List") if "List" in detail_resp.json()["questions"][0]["options"] else 2

        submit_resp = client.post(f"/api/v1/assessments/attempt/{attempt_id}/submit", json={
            "answers": [{"question_id": q_id, "selected_option_index": correct_idx}]
        })
        self.assertEqual(submit_resp.status_code, 200)

        # Check evidence recorded with ASSESSMENT source and verified status
        ev_resp = client.get("/api/v1/student/evidence")
        evidence = ev_resp.json()
        ass_ev = next((e for e in evidence if e["source"] == "ASSESSMENT"), None)
        self.assertIsNotNone(ass_ev)
        self.assertEqual(ass_ev["verification_status"], "verified")

if __name__ == "__main__":
    unittest.main()
