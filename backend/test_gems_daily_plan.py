import pytest
from datetime import date
from app.core.database import SessionLocal
from app.models import User, Student, TargetCompany, CareerRole, StudentCareerGoal, Skill, TargetCompanyRole, TargetCompanyRoleSkill, GemsDailyPlan, GemsTask
from app.services.achiever_roadmap import generate_student_roadmap
from app.services.gems_daily_plan import get_or_generate_daily_plan, update_task_status, get_help_context

def test_gems_daily_plan():
    db = SessionLocal()
    try:
        # User & Student
        user = db.query(User).filter_by(email="gems_test@example.com").first()
        if not user:
            user = User(firebase_uid="gems_test_uid", email="gems_test@example.com")
            db.add(user)
            db.commit()

        student = db.query(Student).filter_by(user_id=user.id).first()
        if not student:
            student = Student(user_id=user.id, full_name="Gems Test Student")
            db.add(student)
            db.commit()

        # Target Goal
        company = db.query(TargetCompany).filter_by(name="GemsCompany").first()
        if not company:
            company = TargetCompany(name="GemsCompany", normalized_name="gemscompany")
            db.add(company)
            db.commit()

        role = db.query(CareerRole).filter_by(name="GemsRole").first()
        if not role:
            role = CareerRole(name="GemsRole")
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

        # Skill & Requirement
        skill = db.query(Skill).filter_by(name="GemsSkill").first()
        if not skill:
            skill = Skill(name="GemsSkill", category_id=1)
            db.add(skill)
            db.commit()

        comp_role = db.query(TargetCompanyRole).filter_by(company_id=company.id, career_role_id=role.id).first()
        if not comp_role:
            comp_role = TargetCompanyRole(company_id=company.id, career_role_id=role.id)
            db.add(comp_role)
            db.commit()
            db.add(TargetCompanyRoleSkill(target_company_role_id=comp_role.id, skill_id=skill.id, required_proficiency_level=4))
            db.commit()

        # 1. Clean missing/roadmap state
        db.query(GemsTask).delete()
        db.query(GemsDailyPlan).delete()
        db.commit()

        # 2. Test empty generation (No roadmap)
        empty_plan = get_or_generate_daily_plan(db, student)
        # We need a roadmap first. Wait, empty plan should be None or handle it.
        # It's None since no roadmap exists. (Well, maybe one exists from previous test run if we didn't wipe roadmaps)
        # Let's just generate a roadmap.
        generate_student_roadmap(db, student)

        # 3. Generate daily plan
        plan = get_or_generate_daily_plan(db, student)
        assert plan is not None
        assert plan.plan_date == date.today()
        assert len(plan.tasks) == 3
        assert plan.summary.total == 3
        assert plan.summary.completed == 0

        # Check task types
        task_types = [t.task_type for t in plan.tasks]
        assert "learning" in task_types
        assert "practice" in task_types
        assert "review" in task_types

        # Test duplicate generation returns the same plan
        plan2 = get_or_generate_daily_plan(db, student)
        assert plan2.id == plan.id

        # 4. Task lifecycle
        task_id = plan.tasks[0].id
        
        # Start
        started = update_task_status(db, student, task_id, "in_progress")
        assert started.status == "in_progress"

        # Complete
        completed = update_task_status(db, student, task_id, "completed", "Test note")
        assert completed.status == "completed"
        assert completed.completion_note == "Test note"

        # Skip
        task_id_2 = plan.tasks[1].id
        skipped = update_task_status(db, student, task_id_2, "skipped", "Too hard")
        assert skipped.status == "skipped"

        # Help Context
        help_ctx = get_help_context(db, student, task_id_2)
        assert help_ctx.task_id == task_id_2
        assert help_ctx.help_available is True

        print("GEMS tests passed successfully!")

    except Exception as e:
        print(f"Test failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    test_gems_daily_plan()
