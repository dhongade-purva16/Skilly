from sqlalchemy.orm import Session
from datetime import datetime
import json
from app.models import Student, Roadmap, RoadmapStep, Skill
from app.schemas.roadmap import RoadmapResponse, RoadmapTarget, RoadmapStepResponse, RoadmapResource
from app.services.achiever_context import build_achiever_context
from app.services.achiever_priority import build_priorities
from app.services.knowledge_retrieval import retrieve_resources_for_skill
from app.services.knowledge_reranker import knowledge_reranker

class DummyRoadmapPersonalizer:
    @staticmethod
    def personalize_step(skill_name: str, role_name: str, gap_status: str, resources: list) -> dict:
        objective = f"Master {skill_name} fundamentals and applications."
        practice_task = f"Build a small project using {skill_name} relevant to a {role_name} role."
        if gap_status == "Missing":
            objective = f"Learn {skill_name} from scratch to meet {role_name} requirements."
            practice_task = f"Complete beginner tutorials and create a basic {skill_name} implementation."
        elif gap_status == "Gap":
            objective = f"Improve {skill_name} proficiency to advance your {role_name} capabilities."
            practice_task = f"Refactor an existing project or build an intermediate feature using {skill_name}."
            
        return {
            "objective": objective,
            "practice_task": practice_task,
            "estimated_duration": "2 weeks" if gap_status == "Missing" else "1 week"
        }

def get_student_roadmap(db: Session, student: Student) -> RoadmapResponse | None:
    context = build_achiever_context(db, student)
    company_id = context.target.target_company.id if context.target.target_company else None
    role_id = context.target.target_role.id if context.target.target_role else None
    
    roadmap = db.query(Roadmap).filter_by(
        student_id=student.id,
        target_company_id=company_id,
        target_role_id=role_id
    ).first()
    
    if not roadmap:
        return None
        
    target_dict = RoadmapTarget(
        company=context.target.target_company.name if context.target.target_company else None,
        role=context.target.target_role.name if context.target.target_role else None
    )
    
    steps = []
    for step in sorted(roadmap.steps, key=lambda x: x.step_order):
        resource_refs = step.resource_references or []
        resources = [RoadmapResource(**r) for r in resource_refs]
        
        steps.append(RoadmapStepResponse(
            id=step.id,
            roadmap_id=step.roadmap_id,
            step_order=step.step_order,
            skill_id=step.skill_id,
            skill_name=step.skill.name if step.skill else "Unknown",
            priority=step.priority,
            objective=step.objective,
            description=step.description,
            estimated_duration=step.estimated_duration,
            resources=resources,
            practice_task=step.practice_task,
            status=step.status
        ))
        
    return RoadmapResponse(
        roadmap_id=roadmap.id,
        target=target_dict,
        summary=roadmap.summary,
        status=roadmap.status,
        steps=steps
    )

def generate_student_roadmap(db: Session, student: Student) -> RoadmapResponse:
    context = build_achiever_context(db, student)
    priorities = build_priorities(db, student, context)
    
    company_id = priorities.target.target_company.id if priorities.target.target_company else None
    role_id = priorities.target.target_role.id if priorities.target.target_role else None
    company_name = priorities.target.target_company.name if priorities.target.target_company else "Unknown Company"
    role_name = priorities.target.target_role.name if priorities.target.target_role else "Unknown Role"
    
    # 1. Clean up existing roadmap for this exact target
    existing = db.query(Roadmap).filter_by(
        student_id=student.id,
        target_company_id=company_id,
        target_role_id=role_id
    ).first()
    if existing:
        from app.models import GemsDailyPlan
        db.query(GemsDailyPlan).filter_by(roadmap_id=existing.id).delete()
        db.delete(existing)
        db.flush()
        
    # 2. Create new roadmap
    roadmap = Roadmap(
        student_id=student.id,
        target_company_id=company_id,
        target_role_id=role_id,
        title=f"Roadmap to {role_name}",
        summary=f"Personalized learning path to close skill gaps for {role_name}" + (f" at {company_name}" if company_id else "")
    )
    db.add(roadmap)
    db.flush()
    
    # 3. Filter and sort gaps
    # Priorities map: HIGH=3, MEDIUM=2, LOW=1
    # Status map: Missing=2, Gap=1
    def sort_key(gap):
        p_score = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(gap.priority, 0)
        s_score = {"Missing": 2, "Gap": 1}.get(gap.gap_status, 0)
        return (p_score, s_score)
        
    actionable_gaps = [g for g in priorities.prioritized_gaps if g.gap_status in ["Missing", "Gap"]]
    sorted_gaps = sorted(actionable_gaps, key=sort_key, reverse=True)
    
    # 4. Generate steps
    step_order = 1
    for gap in sorted_gaps:
        # Determine difficulty for resource search
        difficulty = "beginner"
        if gap.current_proficiency >= 3:
            difficulty = "advanced"
        elif gap.current_proficiency >= 1:
            difficulty = "intermediate"

        query = f"Learn {gap.skill.name} for {role_name}"
        raw_resources = retrieve_resources_for_skill(db, query, gap.skill.id, difficulty, top_k=3)
        if not raw_resources:
            raw_resources = retrieve_resources_for_skill(db, query, gap.skill.id, None, top_k=3)
            
        final_resources = knowledge_reranker.rerank(query, raw_resources)
        
        resource_dicts = []
        for r in final_resources:
            resource_dicts.append({
                "resource_id": r.resource_id,
                "title": r.title,
                "source_url": r.source_url,
                "difficulty": r.difficulty,
                "provider": r.provider
            })
            
        llm_content = DummyRoadmapPersonalizer.personalize_step(
            gap.skill.name, role_name, gap.gap_status, final_resources
        )
        
        step = RoadmapStep(
            roadmap_id=roadmap.id,
            skill_id=gap.skill.id,
            step_order=step_order,
            title=f"Learn {gap.skill.name}",
            objective=llm_content["objective"],
            priority=gap.priority,
            estimated_duration=llm_content["estimated_duration"],
            resource_references=resource_dicts,
            practice_task=llm_content["practice_task"]
        )
        db.add(step)
        step_order += 1
        
    db.commit()
    return get_student_roadmap(db, student)
