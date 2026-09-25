import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import Student, User, StudentEvidence
from app.services.achiever_context import build_achiever_context

def test_evidence_mapping():
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email="evidence_mapping@example.com").first()
        if not user:
            user = User(firebase_uid="ev_test_uid", email="evidence_mapping@example.com")
            db.add(user)
            db.commit()
            
        student = db.query(Student).filter_by(user_id=user.id).first()
        if not student:
            student = Student(user_id=user.id, full_name="Evidence Mapping Student")
            db.add(student)
            db.commit()

        # Clear old evidence for repeatable testing
        db.query(StudentEvidence).filter_by(student_id=student.id).delete()
        db.commit()

        # 1. Evidence with metadata dictionary & 3. Assessment evidence
        ev1 = StudentEvidence(
            student_id=student.id,
            source="ASSESSMENT",
            evidence_type="skill_assessment",
            extracted_data={"score": 95, "time_taken": 30},
            verification_status="VERIFIED"
        )
        db.add(ev1)

        # 2. Evidence with null metadata & 4. Resume evidence & 6. Optional fields
        ev2 = StudentEvidence(
            student_id=student.id,
            source="RESUME",
            evidence_type="document",
            extracted_data=None, # null metadata
            verification_status="UNVERIFIED",
            source_url="http://example.com/resume.pdf",
            confidence=0.8
        )
        db.add(ev2)

        # 5. LinkedIn evidence
        ev3 = StudentEvidence(
            student_id=student.id,
            source="LINKEDIN",
            evidence_type="external_profile",
            extracted_data={"connections": 500},
            verification_status="NOT_SYNCED"
        )
        db.add(ev3)
        db.commit()

        # 7. Context endpoint returns valid Pydantic response
        context = build_achiever_context(db, student)

        assert len(context.evidence) == 3
        
        # Verify ev1
        ctx_ev1 = next(e for e in context.evidence if e.type == "skill_assessment")
        assert ctx_ev1.status == "VERIFIED"
        assert ctx_ev1.metadata == {"score": 95, "time_taken": 30}

        # Verify ev2
        ctx_ev2 = next(e for e in context.evidence if e.type == "document")
        assert ctx_ev2.status == "UNVERIFIED"
        assert ctx_ev2.metadata == {} # Null metadata handled

        # Verify ev3
        ctx_ev3 = next(e for e in context.evidence if e.type == "external_profile")
        assert ctx_ev3.status == "NOT_SYNCED"
        assert ctx_ev3.metadata == {"connections": 500}
        
        print("All evidence mapping tests passed successfully!")

    finally:
        db.close()

if __name__ == "__main__":
    test_evidence_mapping()
