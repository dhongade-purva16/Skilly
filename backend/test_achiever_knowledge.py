import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import (
    Student, User, TargetCompany, CareerRole, TargetCompanyRole, 
    TargetCompanyRoleSkill, CareerRoleSkill, Skill, StudentCareerGoal, StudentSkill,
    KnowledgeResource, KnowledgeChunk
)
from app.services.knowledge_base import ingest_resource
from app.services.knowledge_retrieval import retrieve_resources_for_skill

def test_achiever_knowledge():
    db = SessionLocal()
    try:
        # Create skill
        skill1 = db.query(Skill).filter_by(name="Test Skill KB").first()
        if not skill1:
            skill1 = Skill(name="Test Skill KB", category_id=1)
            db.add(skill1)
            db.commit()

        # Clean existing resources
        db.query(KnowledgeResource).filter(KnowledgeResource.title.like("Test KB %")).delete(synchronize_session=False)
        db.commit()

        # Ingest resources
        r1 = ingest_resource(
            db=db,
            title="Test KB Approved Basic",
            content="This is a test content for basic knowledge.",
            resource_type="article",
            provider="TestProvider",
            source_url="http://test.com/1",
            skill_id=skill1.id,
            difficulty="beginner",
            trust_status="approved"
        )

        r2 = ingest_resource(
            db=db,
            title="Test KB Pending Advanced",
            content="This is a test content for advanced knowledge. " * 20,
            resource_type="course",
            provider="TestProvider",
            source_url="http://test.com/2",
            skill_id=skill1.id,
            difficulty="advanced",
            trust_status="pending"
        )
        
        r3 = ingest_resource(
            db=db,
            title="Test KB Approved Advanced",
            content="This is a test content for approved advanced knowledge. " * 20,
            resource_type="course",
            provider="TestProvider",
            source_url="http://test.com/3",
            skill_id=skill1.id,
            difficulty="advanced",
            trust_status="approved"
        )

        # 1. Check chunks created
        assert len(r1.chunks) > 0
        assert len(r2.chunks) > 0

        # 2. Approved resource is retrievable, pending is NOT
        results = retrieve_resources_for_skill(db, "test content", skill1.id, "beginner")
        assert len(results) == 1
        assert results[0].title == "Test KB Approved Basic"
        
        # 3. Difficulty filtering works
        results_adv = retrieve_resources_for_skill(db, "test content", skill1.id, "advanced")
        assert len(results_adv) == 1
        assert results_adv[0].title == "Test KB Approved Advanced" # r2 is pending so it's not returned
        
        print("Knowledge tests passed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    test_achiever_knowledge()
