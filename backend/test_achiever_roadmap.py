import pytest
from app.core.database import SessionLocal
from app.models import User, Student, TargetCompany, CareerRole, SkillCategory, Skill, StudentCareerGoal, TargetCompanyRole, TargetCompanyRoleSkill, StudentSkill, SkillEvidence
from app.services.achiever_roadmap import generate_student_roadmap, get_student_roadmap

def test_achiever_roadmap():
    db = SessionLocal()
    try:
        # Create test user and student
        user = db.query(User).filter_by(email="roadmap_test@example.com").first()
        if not user:
            user = User(firebase_uid="roadmap_test_uid", email="roadmap_test@example.com")
            db.add(user)
            db.commit()

        student = db.query(Student).filter_by(user_id=user.id).first()
        if not student:
            student = Student(user_id=user.id, full_name="Roadmap Test Student")
            db.add(student)
            db.commit()

        # Add target company and role
        company = db.query(TargetCompany).filter_by(name="RoadmapTestCompany").first()
        if not company:
            company = TargetCompany(name="RoadmapTestCompany", normalized_name="roadmaptestcompany")
            db.add(company)
            db.commit()

        role = db.query(CareerRole).filter_by(name="RoadmapTester").first()
        if not role:
            role = CareerRole(name="RoadmapTester")
            db.add(role)
            db.commit()

        goal = db.query(StudentCareerGoal).filter_by(student_id=student.id).first()
        if not goal:
            goal = StudentCareerGoal(student_id=student.id, career_role_id=role.id, target_company_id=company.id)
            db.add(goal)
            db.commit()
        else:
            goal.career_role_id = role.id
            goal.target_company_id = company.id
            db.commit()

        # Add skills
        skill1 = db.query(Skill).filter_by(name="Roadmap Missing Skill").first()
        if not skill1:
            skill1 = Skill(name="Roadmap Missing Skill", category_id=1)
            db.add(skill1)
            db.commit()

        skill2 = db.query(Skill).filter_by(name="Roadmap Gap Skill").first()
        if not skill2:
            skill2 = Skill(name="Roadmap Gap Skill", category_id=1)
            db.add(skill2)
            db.commit()

        skill3 = db.query(Skill).filter_by(name="Roadmap Sufficient Skill").first()
        if not skill3:
            skill3 = Skill(name="Roadmap Sufficient Skill", category_id=1)
            db.add(skill3)
            db.commit()

        # Add requirements
        comp_role = db.query(TargetCompanyRole).filter_by(company_id=company.id, career_role_id=role.id).first()
        if not comp_role:
            comp_role = TargetCompanyRole(company_id=company.id, career_role_id=role.id)
            db.add(comp_role)
            db.commit()

            db.add(TargetCompanyRoleSkill(target_company_role_id=comp_role.id, skill_id=skill1.id, required_proficiency_level=3))
            db.add(TargetCompanyRoleSkill(target_company_role_id=comp_role.id, skill_id=skill2.id, required_proficiency_level=3))
            db.add(TargetCompanyRoleSkill(target_company_role_id=comp_role.id, skill_id=skill3.id, required_proficiency_level=3))
            db.commit()

        # Add student skills
        ss2 = db.query(StudentSkill).filter_by(student_id=student.id, skill_id=skill2.id).first()
        if not ss2:
            ss2 = StudentSkill(student_id=student.id, skill_id=skill2.id, proficiency_level=1)
            db.add(ss2)
            db.commit()
        else:
            ss2.proficiency_level = 1
            db.commit()

        ss3 = db.query(StudentSkill).filter_by(student_id=student.id, skill_id=skill3.id).first()
        if not ss3:
            ss3 = StudentSkill(student_id=student.id, skill_id=skill3.id, proficiency_level=3)
            db.add(ss3)
            db.commit()
        else:
            ss3.proficiency_level = 3
            db.commit()

        # Generate roadmap
        roadmap = generate_student_roadmap(db, student)

        assert roadmap is not None
        assert roadmap.target.company == "RoadmapTestCompany"
        assert roadmap.target.role == "RoadmapTester"
        assert len(roadmap.steps) == 2  # Sufficient skill should be omitted

        # Check order: Missing (High Priority) before Gap
        assert roadmap.steps[0].skill_name == "Roadmap Missing Skill"
        assert roadmap.steps[0].priority == "HIGH"
        assert roadmap.steps[1].skill_name == "Roadmap Gap Skill"

        # Check retrieval
        fetched = get_student_roadmap(db, student)
        assert fetched is not None
        assert fetched.roadmap_id == roadmap.roadmap_id
        
        # Test duplicate generation doesn't duplicate the roadmap
        roadmap2 = generate_student_roadmap(db, student)
        assert roadmap2.roadmap_id != roadmap.roadmap_id
        assert len(roadmap2.steps) == 2

        print("Roadmap tests passed successfully!")

    except Exception as e:
        print(f"Test failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    test_achiever_roadmap()
