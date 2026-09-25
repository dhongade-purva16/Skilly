from typing import List
from sqlalchemy.orm import Session
from app.models import Student
from app.schemas.achiever import AchieverContextResponse, PrioritizedSkillGap, AchieverPriorityResponse, EvidenceSummaryItem
from app.services.achiever_evidence import EvidenceIntelligence

def determine_gap_priority(gap, evidence_summary, metadata) -> tuple[str, List[str]]:
    reasons = []
    
    # 1. Check if completely missing
    is_missing = (gap.current_proficiency == 0)
    
    # 2. Check gap severity
    severity = gap.required_proficiency - gap.current_proficiency
    
    if is_missing:
        reasons.append("Skill is completely missing.")
        priority = "HIGH"
    elif severity > 0:
        reasons.append(f"Current proficiency ({gap.current_proficiency}) is below required proficiency ({gap.required_proficiency}).")
        if severity >= 2:
            priority = "HIGH"
        else:
            priority = "MEDIUM"
    else:
        reasons.append("Proficiency meets or exceeds requirements.")
        priority = "LOW"

    if gap.requirement_source == "company_specific":
        reasons.append("Skill is a company-specific requirement.")
        if priority == "MEDIUM":
            priority = "HIGH"
            
    return priority, reasons

def build_priorities(db: Session, student: Student, context: AchieverContextResponse) -> AchieverPriorityResponse:
    evidence_intel = EvidenceIntelligence(db, student, context)
    
    prioritized_gaps = []
    
    for gap in context.skill_gaps:
        # Get evidence summary
        raw_evidence = evidence_intel.get_skill_evidence_summary(gap.skill.id)
        evidence_summary = [EvidenceSummaryItem(source=e["source"], status=e["status"]) for e in raw_evidence]
        
        # Dependency Status
        dependency_status = "not_available"
        
        # Priority Logic
        priority, reasons = determine_gap_priority(gap, evidence_summary, context.metadata)
        
        prioritized_gaps.append(
            PrioritizedSkillGap(
                skill=gap.skill,
                required_proficiency=gap.required_proficiency,
                current_proficiency=gap.current_proficiency,
                gap_status=gap.status,
                priority=priority,
                requirement_source=gap.requirement_source,
                evidence_summary=evidence_summary,
                dependency_status=dependency_status,
                reasons=reasons
            )
        )
        
    summary = "Priority analysis completed successfully."
    if not prioritized_gaps:
        if not context.metadata.has_target_role:
            summary = "Select a target job role to generate skill priorities."
        else:
            summary = "No current skill gaps detected from the available assessment data."
            
    return AchieverPriorityResponse(
        target=context.target,
        requirement_source=context.metadata.requirement_source,
        prioritized_gaps=prioritized_gaps,
        summary=summary
    )
