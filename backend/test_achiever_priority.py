import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Student, User, Skill, StudentSkill, SkillEvidence, TargetCompany, CareerRole, StudentCareerGoal, TargetCompanyRole, TargetCompanyRoleSkill
from app.services.achiever_context import build_achiever_context
from app.services.achiever_priority import build_priorities

def test_achiever_priority():
    db = SessionLocal()
    try:
        # Create test user and student
        user = db.query(User).filter_by(email="priority_test@example.com").first()
        if not user:
            user = User(firebase_uid="priority_test_uid", email="priority_test@example.com")
            db.add(user)
            db.commit()
            
        student = db.query(Student).filter_by(user_id=user.id).first()
        if not student:
            student = Student(user_id=user.id, full_name="Priority Test Student")
            db.add(student)
            db.commit()
            
        # 1-2. Authenticated student request logic (mocked by DB fetch)
        # 3. No target role initially
        context = build_achiever_context(db, student)
        priorities = build_priorities(db, student, context)
        assert priorities.summary == "Select a target job role to generate skill priorities."
        assert len(priorities.prioritized_gaps) == 0

        # Setup target role and company
        role = db.query(CareerRole).filter_by(name="Test Role Priority").first()
        if not role:
            role = CareerRole(name="Test Role Priority")
            db.add(role)
            db.commit()
            
        company = db.query(TargetCompany).filter_by(name="Test Company Priority").first()
        if not company:
            company = TargetCompany(name="Test Company Priority", normalized_name="test company priority")
            db.add(company)
            db.commit()

        goal = student.career_goal
        if not goal:
            goal = StudentCareerGoal(student_id=student.id, career_role_id=role.id, target_company_id=company.id)
            db.add(goal)
            db.commit()
        else:
            goal.career_role_id = role.id
            goal.target_company_id = company.id
            db.commit()

        # Add skills
        skill1 = db.query(Skill).filter_by(name="Priority Missing Skill").first()
        if not skill1:
            skill1 = Skill(name="Priority Missing Skill", category_id=1)
            db.add(skill1)
            db.commit()
            
        skill2 = db.query(Skill).filter_by(name="Priority Gap Skill").first()
        if not skill2:
            skill2 = Skill(name="Priority Gap Skill", category_id=1)
            db.add(skill2)
            db.commit()
            
        skill3 = db.query(Skill).filter_by(name="Priority Sufficient Skill").first()
        if not skill3:
            skill3 = Skill(name="Priority Sufficient Skill", category_id=1)
            db.add(skill3)
            db.commit()

        # Add requirements (Company specific)
        comp_role = db.query(TargetCompanyRole).filter_by(company_id=company.id, career_role_id=role.id).first()
        if not comp_role:
            comp_role = TargetCompanyRole(company_id=company.id, career_role_id=role.id)
            db.add(comp_role)
            db.commit()
            
            db.add(TargetCompanyRoleSkill(target_company_role_id=comp_role.id, skill_id=skill1.id, required_proficiency_level=3))
            db.add(TargetCompanyRoleSkill(target_company_role_id=comp_role.id, skill_id=skill2.id, required_proficiency_level=3))
            db.add(TargetCompanyRoleSkill(target_company_role_id=comp_role.id, skill_id=skill3.id, required_proficiency_level=3))
            db.commit()

        # 4. Student with Target Role & 5. Company Specific Requirements
        context = build_achiever_context(db, student)
        assert context.metadata.requirement_source == "company_specific"
        
        # Add student skills (Current proficiencies)
        # Missing skill = no student skill
        
        # Gap skill = level 1, required 3
        ss2 = db.query(StudentSkill).filter_by(student_id=student.id, skill_id=skill2.id).first()
        if not ss2:
            ss2 = StudentSkill(student_id=student.id, skill_id=skill2.id, proficiency_level=1)
            db.add(ss2)
            
            # Add Unverified evidence (Resume) for Gap skill
            se2 = SkillEvidence(student_id=student.id, skill_id=skill2.id, source_type="Resume", evidence_score=0.5)
            db.add(se2)
            db.commit()
            
        # Sufficient skill = level 3, required 3
        ss3 = db.query(StudentSkill).filter_by(student_id=student.id, skill_id=skill3.id).first()
        if not ss3:
            ss3 = StudentSkill(student_id=student.id, skill_id=skill3.id, proficiency_level=3)
            db.add(ss3)
            
            # Add Verified evidence (Assessment) for Sufficient skill
            se3 = SkillEvidence(student_id=student.id, skill_id=skill3.id, source_type="Assessment", evidence_score=1.0)
            db.add(se3)
            db.commit()
            
        # 6. Run Priorities again
        context = build_achiever_context(db, student)
        priorities = build_priorities(db, student, context)
        
        print("Summary:", priorities.summary)
        print("Requirement Source:", priorities.requirement_source)
        
        for p in priorities.prioritized_gaps:
            print(f"Skill: {p.skill.name}")
            print(f"Gap Status: {p.gap_status}")
            print(f"Priority: {p.priority}")
            print(f"Reasons: {p.reasons}")
            print(f"Evidence: {p.evidence_summary}")
            print("-----")
            
        assert len(priorities.prioritized_gaps) == 3
        
        # Checks for missing skill
        p_missing = next(p for p in priorities.prioritized_gaps if p.skill.id == skill1.id)
        assert p_missing.gap_status == "Missing"
        assert p_missing.priority == "HIGH"
        assert any("missing" in r for r in p_missing.reasons)
        assert len(p_missing.evidence_summary) == 0
        
        # Checks for gap skill
        p_gap = next(p for p in priorities.prioritized_gaps if p.skill.id == skill2.id)
        assert p_gap.gap_status == "Gap"
        assert p_gap.priority == "HIGH" # company specific requirement elevates medium to high
        assert len(p_gap.evidence_summary) == 1
        assert p_gap.evidence_summary[0].source == "Resume"
        assert p_gap.evidence_summary[0].status == "UNVERIFIED"
        
        # Checks for sufficient skill
        p_suff = next(p for p in priorities.prioritized_gaps if p.skill.id == skill3.id)
        assert p_suff.gap_status == "Sufficient"
        assert p_suff.priority == "LOW"
        assert len(p_suff.evidence_summary) == 1
        assert p_suff.evidence_summary[0].source == "Assessment"
        assert p_suff.evidence_summary[0].status == "VERIFIED"
        
        print("All priority tests passed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    test_achiever_priority()
