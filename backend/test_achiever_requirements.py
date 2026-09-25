import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import (
    Student, User, TargetCompany, CareerRole, TargetCompanyRole, 
    TargetCompanyRoleSkill, CareerRoleSkill, Skill, StudentCareerGoal, StudentSkill
)
from app.services.achiever_context import build_achiever_context

def test_achiever_requirements():
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email="requirements_test@example.com").first()
        if not user:
            user = User(firebase_uid="req_test_uid", email="requirements_test@example.com")
            db.add(user)
            db.commit()
            
        student = db.query(Student).filter_by(user_id=user.id).first()
        if not student:
            student = Student(user_id=user.id, full_name="Req Test Student")
            db.add(student)
            db.commit()

        # Clear career goal
        if student.career_goal:
            db.delete(student.career_goal)
            db.commit()

        # Create basic test data
        skill1 = db.query(Skill).filter_by(name="Req Skill 1").first()
        if not skill1:
            skill1 = Skill(name="Req Skill 1", category_id=1)
            db.add(skill1)
            db.commit()

        # 5. Missing role -> no requirements
        context = build_achiever_context(db, student)
        assert context.metadata.requirement_source == "none"

        # Set up role
        role = db.query(CareerRole).filter_by(name="Req Test Role").first()
        if not role:
            role = CareerRole(name="Req Test Role")
            db.add(role)
            db.commit()

        goal = StudentCareerGoal(student_id=student.id, career_role_id=role.id)
        db.add(goal)
        db.commit()

        # 6. Role exists but has no requirements
        context = build_achiever_context(db, student)
        assert context.metadata.requirement_source == "none"
        
        # 3. Role-only target (Add Role requirements)
        crs = db.query(CareerRoleSkill).filter_by(career_role_id=role.id).first()
        if not crs:
            db.add(CareerRoleSkill(career_role_id=role.id, skill_id=skill1.id, required_proficiency_level=4))
            db.commit()
            
        context = build_achiever_context(db, student)
        assert context.metadata.requirement_source == "role_fallback"
        assert len(context.requirements) == 1

        # 4. Missing company (Already tested above, since company is null and role has requirements)
        
        # Setup company
        company = db.query(TargetCompany).filter_by(name="Req Test Company").first()
        if not company:
            company = TargetCompany(name="Req Test Company", normalized_name="req test company")
            db.add(company)
            db.commit()

        goal.target_company_id = company.id
        db.commit()

        # 7. Company exists but company-specific requirements do not -> role_fallback
        context = build_achiever_context(db, student)
        assert context.metadata.requirement_source == "role_fallback"

        # Setup company specific requirements
        comp_role = db.query(TargetCompanyRole).filter_by(company_id=company.id, career_role_id=role.id).first()
        if not comp_role:
            comp_role = TargetCompanyRole(company_id=company.id, career_role_id=role.id)
            db.add(comp_role)
            db.commit()
            
            db.add(TargetCompanyRoleSkill(target_company_role_id=comp_role.id, skill_id=skill1.id, required_proficiency_level=5))
            db.commit()

        # 1. Company-specific requirements exist & 8. Requirements map to valid skills
        context = build_achiever_context(db, student)
        assert context.metadata.requirement_source == "company_specific"
        assert len(context.requirements) == 1
        assert context.requirements[0].required_proficiency == 5 # Overrode the fallback 4

        # 9, 10, 11: StudentSkill Missing, Gap, Sufficient
        db.query(StudentSkill).filter_by(student_id=student.id).delete()
        db.commit()
        
        # Missing
        context = build_achiever_context(db, student)
        assert context.skill_gaps[0].status == "Missing"
        
        # Gap
        ss = StudentSkill(student_id=student.id, skill_id=skill1.id, proficiency_level=3)
        db.add(ss)
        db.commit()
        context = build_achiever_context(db, student)
        assert context.skill_gaps[0].status == "Gap"
        
        # Sufficient
        ss.proficiency_level = 5
        db.commit()
        context = build_achiever_context(db, student)
        assert context.skill_gaps[0].status == "Sufficient"

        print("All requirement context tests passed successfully!")

    finally:
        db.close()

if __name__ == "__main__":
    test_achiever_requirements()
