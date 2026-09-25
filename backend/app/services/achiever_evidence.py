from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.schemas.achiever import AchieverContextResponse
from app.models import SkillEvidence, Student

class EvidenceIntelligence:
    def __init__(self, db: Session, student: Student, context: AchieverContextResponse):
        self.db = db
        self.student = student
        self.context = context

    def get_skill_evidence_summary(self, skill_id: int) -> List[Dict[str, str]]:
        # Find explicit skill evidence from DB
        skill_evidences = self.db.query(SkillEvidence).filter(
            SkillEvidence.student_id == self.student.id,
            SkillEvidence.skill_id == skill_id
        ).all()

        summary = []
        if skill_evidences:
            for ev in skill_evidences:
                source = ev.source_type or "Unknown"
                status = "UNVERIFIED"
                if source.upper() == "ASSESSMENT":
                    status = "VERIFIED"
                summary.append({
                    "source": source,
                    "status": status
                })
        
        return summary

