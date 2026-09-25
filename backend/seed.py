import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import (
    SkillCategory, Skill, Assessment, AssessmentQuestion, CareerRole, CareerRoleSkill,
    TargetCompany, TargetCompanyRole, TargetCompanyRoleSkill
)

def seed_db():
    db: Session = SessionLocal()
    try:
        # 1. Categories
        cat_tech = db.query(SkillCategory).filter(SkillCategory.name == "Technical").first()
        if not cat_tech:
            cat_tech = SkillCategory(name="Technical")
            db.add(cat_tech)
            db.commit()
            db.refresh(cat_tech)
            
        cat_soft = db.query(SkillCategory).filter(SkillCategory.name == "Soft Skills").first()
        if not cat_soft:
            cat_soft = SkillCategory(name="Soft Skills")
            db.add(cat_soft)
            db.commit()
            db.refresh(cat_soft)

        # 2. Skills
        skills_def = [
            ("Python", cat_tech.id),
            ("PostgreSQL", cat_tech.id),
            ("React", cat_tech.id),
            ("TypeScript", cat_tech.id),
            ("FastAPI", cat_tech.id),
            ("Communication", cat_soft.id),
            ("Group Discussion", cat_soft.id),
            ("Presentation", cat_soft.id),
            ("Problem Solving", cat_soft.id)
        ]
        skill_objs = {}
        for sname, cid in skills_def:
            sobj = db.query(Skill).filter(Skill.name == sname).first()
            if not sobj:
                sobj = Skill(name=sname, category_id=cid)
                db.add(sobj)
                db.commit()
                db.refresh(sobj)
            skill_objs[sname] = sobj

        # 3. Career Roles
        roles_def = [
            ("Backend Developer", "Develops backend services and APIs."),
            ("Frontend Developer", "Builds modern user interfaces."),
            ("Data Scientist", "Analyzes data and builds machine learning models."),
            ("Full Stack Developer", "Works on both frontend and backend technologies.")
        ]
        role_objs = {}
        for rname, rdesc in roles_def:
            robj = db.query(CareerRole).filter(CareerRole.name == rname).first()
            if not robj:
                robj = CareerRole(name=rname, description=rdesc)
                db.add(robj)
                db.commit()
                db.refresh(robj)
            role_objs[rname] = robj

        # 4. Standard Role Skills (CareerRoleSkill)
        backend_role = role_objs["Backend Developer"]
        crs_py = db.query(CareerRoleSkill).filter(CareerRoleSkill.career_role_id == backend_role.id, CareerRoleSkill.skill_id == skill_objs["Python"].id).first()
        if not crs_py:
            db.add(CareerRoleSkill(career_role_id=backend_role.id, skill_id=skill_objs["Python"].id, required_proficiency_level=4))
        crs_pg = db.query(CareerRoleSkill).filter(CareerRoleSkill.career_role_id == backend_role.id, CareerRoleSkill.skill_id == skill_objs["PostgreSQL"].id).first()
        if not crs_pg:
            db.add(CareerRoleSkill(career_role_id=backend_role.id, skill_id=skill_objs["PostgreSQL"].id, required_proficiency_level=3))
        crs_ps = db.query(CareerRoleSkill).filter(CareerRoleSkill.career_role_id == backend_role.id, CareerRoleSkill.skill_id == skill_objs["Problem Solving"].id).first()
        if not crs_ps:
            db.add(CareerRoleSkill(career_role_id=backend_role.id, skill_id=skill_objs["Problem Solving"].id, required_proficiency_level=4))

        frontend_role = role_objs["Frontend Developer"]
        crs_react = db.query(CareerRoleSkill).filter(CareerRoleSkill.career_role_id == frontend_role.id, CareerRoleSkill.skill_id == skill_objs["React"].id).first()
        if not crs_react:
            db.add(CareerRoleSkill(career_role_id=frontend_role.id, skill_id=skill_objs["React"].id, required_proficiency_level=3))
        crs_ts = db.query(CareerRoleSkill).filter(CareerRoleSkill.career_role_id == frontend_role.id, CareerRoleSkill.skill_id == skill_objs["TypeScript"].id).first()
        if not crs_ts:
            db.add(CareerRoleSkill(career_role_id=frontend_role.id, skill_id=skill_objs["TypeScript"].id, required_proficiency_level=3))
        crs_comm = db.query(CareerRoleSkill).filter(CareerRoleSkill.career_role_id == frontend_role.id, CareerRoleSkill.skill_id == skill_objs["Communication"].id).first()
        if not crs_comm:
            db.add(CareerRoleSkill(career_role_id=frontend_role.id, skill_id=skill_objs["Communication"].id, required_proficiency_level=4))

        db.commit()

        # 5. Target Companies
        companies_def = [
            ("Google", "google", "https://google.com", "Global technology company."),
            ("Microsoft", "microsoft", "https://microsoft.com", "Leading software provider."),
            ("TCS", "tcs", "https://tcs.com", "Global IT services and consulting."),
            ("Amazon", "amazon", "https://amazon.com", "E-commerce and cloud computing leader."),
            ("Infosys", "infosys", "https://infosys.com", "Next-generation digital services.")
        ]
        comp_objs = {}
        for cname, norm_name, site, desc in companies_def:
            cobj = db.query(TargetCompany).filter(TargetCompany.normalized_name == norm_name).first()
            if not cobj:
                cobj = TargetCompany(name=cname, normalized_name=norm_name, website=site, description=desc, active=True, source="SEED")
                db.add(cobj)
                db.commit()
                db.refresh(cobj)
            comp_objs[cname] = cobj

        # 6. Target Company Roles & Company-Specific Skill Requirements
        for cname, cobj in comp_objs.items():
            for rname, robj in role_objs.items():
                tcr = db.query(TargetCompanyRole).filter(
                    TargetCompanyRole.company_id == cobj.id,
                    TargetCompanyRole.career_role_id == robj.id
                ).first()
                if not tcr:
                    tcr = TargetCompanyRole(company_id=cobj.id, career_role_id=robj.id)
                    db.add(tcr)
                    db.commit()

        # Google + Backend Developer: Has company-specific skill requirements!
        google_obj = comp_objs["Google"]
        tcr_google_backend = db.query(TargetCompanyRole).filter(
            TargetCompanyRole.company_id == google_obj.id,
            TargetCompanyRole.career_role_id == backend_role.id
        ).first()

        tcrs_py = db.query(TargetCompanyRoleSkill).filter(
            TargetCompanyRoleSkill.target_company_role_id == tcr_google_backend.id,
            TargetCompanyRoleSkill.skill_id == skill_objs["Python"].id
        ).first()
        if not tcrs_py:
            db.add(TargetCompanyRoleSkill(target_company_role_id=tcr_google_backend.id, skill_id=skill_objs["Python"].id, required_proficiency_level=5))
            db.add(TargetCompanyRoleSkill(target_company_role_id=tcr_google_backend.id, skill_id=skill_objs["PostgreSQL"].id, required_proficiency_level=4))
            db.add(TargetCompanyRoleSkill(target_company_role_id=tcr_google_backend.id, skill_id=skill_objs["FastAPI"].id, required_proficiency_level=4))
            db.commit()

        # Google + Frontend Developer: Has company-specific skill requirements!
        tcr_google_frontend = db.query(TargetCompanyRole).filter(
            TargetCompanyRole.company_id == google_obj.id,
            TargetCompanyRole.career_role_id == frontend_role.id
        ).first()

        tcrs_react = db.query(TargetCompanyRoleSkill).filter(
            TargetCompanyRoleSkill.target_company_role_id == tcr_google_frontend.id,
            TargetCompanyRoleSkill.skill_id == skill_objs["React"].id
        ).first()
        if not tcrs_react:
            db.add(TargetCompanyRoleSkill(target_company_role_id=tcr_google_frontend.id, skill_id=skill_objs["React"].id, required_proficiency_level=4))
            db.add(TargetCompanyRoleSkill(target_company_role_id=tcr_google_frontend.id, skill_id=skill_objs["TypeScript"].id, required_proficiency_level=5))
            db.commit()


        # 7. Assessments
        # Standard Assessment (Role Fallback)
        assessment_py = db.query(Assessment).filter(Assessment.title == "Python Fundamentals").first()
        if not assessment_py:
            assessment_py = Assessment(
                skill_id=skill_objs["Python"].id,
                title="Python Fundamentals",
                description="Test your core Python programming knowledge."
            )
            db.add(assessment_py)
            db.commit()
            db.refresh(assessment_py)

            q1 = AssessmentQuestion(
                assessment_id=assessment_py.id,
                question_text="Which data type is mutable in Python?",
                options=["Tuple", "String", "List", "Integer"],
                correct_option_index=2,
                difficulty=1
            )
            q2 = AssessmentQuestion(
                assessment_id=assessment_py.id,
                question_text="What is the result of 2 ** 3 in Python?",
                options=["6", "8", "9", "Error"],
                correct_option_index=1,
                difficulty=1
            )
            db.add_all([q1, q2])
            db.commit()

        # Company-Specific Assessment (Google Python Specialist)
        assessment_google_py = db.query(Assessment).filter(Assessment.title == "Google Python Advanced Assessment").first()
        if not assessment_google_py:
            assessment_google_py = Assessment(
                skill_id=skill_objs["Python"].id,
                target_company_id=google_obj.id,
                title="Google Python Advanced Assessment",
                description="Advanced Python skills required for Google engineering."
            )
            db.add(assessment_google_py)
            db.commit()
            db.refresh(assessment_google_py)

            q1 = AssessmentQuestion(
                assessment_id=assessment_google_py.id,
                question_text="How does Python's Global Interpreter Lock (GIL) affect threads?",
                options=["Prevents multi-threading entirely", "Executes only one thread's bytecode at a time", "Speeds up CPU-bound tasks", "Disables memory management"],
                correct_option_index=1,
                difficulty=3
            )
            db.add(q1)
            db.commit()

        # 8. Knowledge Resources
        from app.services.knowledge_base import ingest_resource

        # Python Resources
        ingest_resource(
            db=db,
            title="Python Crash Course for Beginners",
            content="This is a comprehensive crash course for Python beginners. Learn variables, loops, functions, and data structures.",
            resource_type="course",
            provider="FreeCodeCamp",
            source_url="https://www.freecodecamp.org/news/python-crash-course/",
            skill_id=skill_objs["Python"].id,
            difficulty="beginner",
            estimated_duration="2 hours",
            trust_status="approved"
        )

        ingest_resource(
            db=db,
            title="Advanced Python Generators and Decorators",
            content="Master advanced Python concepts like generators, decorators, context managers, and metaclasses.",
            resource_type="article",
            provider="RealPython",
            source_url="https://realpython.com/advanced-python/",
            skill_id=skill_objs["Python"].id,
            difficulty="advanced",
            estimated_duration="45 mins",
            trust_status="approved"
        )

        # React Resources
        ingest_resource(
            db=db,
            title="React Official Tutorial",
            content="Learn React by building a Tic-Tac-Toe game. Understand components, props, state, and hooks.",
            resource_type="tutorial",
            provider="React Docs",
            source_url="https://react.dev/learn/tutorial-tic-tac-toe",
            skill_id=skill_objs["React"].id,
            difficulty="beginner",
            estimated_duration="1 hour",
            trust_status="approved"
        )

        # TypeScript Resources
        ingest_resource(
            db=db,
            title="TypeScript for JavaScript Programmers",
            content="Learn how TypeScript adds static typing to JavaScript. Interface, type aliases, union types, and generics.",
            resource_type="documentation",
            provider="TypeScript Docs",
            source_url="https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html",
            skill_id=skill_objs["TypeScript"].id,
            difficulty="intermediate",
            estimated_duration="30 mins",
            trust_status="approved"
        )
        
        # Untrusted/Pending resource
        ingest_resource(
            db=db,
            title="Random Python Tricks",
            content="Some random tricks from a forum.",
            resource_type="article",
            provider="Unknown",
            source_url="https://example.com/python-tricks",
            skill_id=skill_objs["Python"].id,
            difficulty="beginner",
            trust_status="pending"
        )

        print("Database seeded with canonical roles, skills, companies, company skills, and assessments successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
