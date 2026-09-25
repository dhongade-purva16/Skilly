from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Dict, Any

from app.models import (
    Student, StudentSkill, SkillEvidence, StudentEvidence, 
    TargetCompanyRole, TargetCompanyRoleSkill, CareerRoleSkill, TargetCompany
)
from app.schemas.achiever import (
    AchieverContextResponse, AchieverStudentContext, AchieverAcademicContext,
    AchieverProfessionalContext, AchieverTargetContext, AchieverTargetCompanyRoleContext,
    AchieverExternalProfilesContext, AchieverResumeContext, AchieverEvidenceContext,
    AchieverSkillContext, AchieverRequirementContext, AchieverSkillGapContext, AchieverMetadataContext
)
from app.schemas.skill import SkillResponse

def build_achiever_context(db: Session, student: Student) -> AchieverContextResponse:
    # 1. Student Context
    student_ctx = AchieverStudentContext(
        full_name=student.full_name,
        phone=student.phone,
        location=student.location,
        bio=student.bio
    )
    
    # 2. Academic Context
    acad = student.academic_profile
    acad_ctx = AchieverAcademicContext()
    if acad:
        acad_ctx = AchieverAcademicContext(
            degree=acad.degree,
            branch=acad.branch,
            academic_year=acad.academic_year,
            graduation_year=acad.graduation_year
        )
        
    # 3. Professional Context
    prof = student.professional_profile
    prof_ctx = AchieverProfessionalContext()
    if prof:
        prof_ctx = AchieverProfessionalContext(
            headline=prof.headline,
            current_status=prof.current_status,
            experience_level=prof.experience_level,
            years_of_experience=prof.years_of_experience,
            professional_summary=prof.professional_summary,
            work_domain=prof.work_domain
        )
        
    # 4 & 5 & 6. Target Context & Requirements Source
    target_ctx = AchieverTargetContext()
    career_goal = student.career_goal
    requirement_source = "none"
    required_skills = []
    
    has_target_company = False
    has_target_role = False
    
    if career_goal and career_goal.career_role_id:
        cr = career_goal.career_role
        target_ctx.career_role = AchieverTargetCompanyRoleContext(
            id=cr.id, name=cr.name, description=cr.description
        )
        has_target_role = True
        
        target_company_id = career_goal.target_company_id
        if target_company_id:
            tc = career_goal.target_company
            target_ctx.target_company = AchieverTargetCompanyRoleContext(
                id=tc.id, name=tc.name, description=tc.description
            )
            has_target_company = True
            
            comp_role = db.query(TargetCompanyRole).filter(
                TargetCompanyRole.company_id == target_company_id,
                TargetCompanyRole.career_role_id == career_goal.career_role_id
            ).first()
            
            if comp_role:
                comp_skills = db.query(TargetCompanyRoleSkill).filter(
                    TargetCompanyRoleSkill.target_company_role_id == comp_role.id
                ).all()
                if comp_skills:
                    required_skills = comp_skills
                    requirement_source = "company_specific"
                    target_ctx.target_role = target_ctx.career_role # conceptually same here
                    
        if requirement_source != "company_specific":
            cr_skills = db.query(CareerRoleSkill).filter(
                CareerRoleSkill.career_role_id == career_goal.career_role_id
            ).all()
            if cr_skills:
                required_skills = cr_skills
                requirement_source = "role_fallback"

    req_ctx_list = []
    for req in required_skills:
        if not req.skill:
            raise ValueError(f"Data integrity error: Requirement references missing skill (skill_id: {req.skill_id})")
        req_ctx_list.append(AchieverRequirementContext(
            skill=SkillResponse.model_validate(req.skill),
            required_proficiency=req.required_proficiency_level,
            source=requirement_source
        ))

    # 7. External Profiles Context
    ext = student.external_profiles
    ext_ctx = AchieverExternalProfilesContext(
        github_status="not_synced",
        linkedin_status="not_synced",
        portfolio_status="not_synced"
    )
    if ext:
        if ext.github_url:
            ext_ctx.github_url = ext.github_url
            ext_ctx.github_status = "url_only"
        if ext.linkedin_url:
            ext_ctx.linkedin_url = ext.linkedin_url
            ext_ctx.linkedin_status = "url_only"
        if ext.portfolio_url:
            ext_ctx.portfolio_url = ext.portfolio_url
            ext_ctx.portfolio_status = "url_only"
            
    has_github = False
    has_linkedin = False
    has_portfolio = False
            
    # 8 & 9. Resume Context
    res_ctx = AchieverResumeContext(extraction_status="not_available")
    has_resume = False
    has_resume_text = False
    
    if student.resumes:
        # Get active resume
        active_res = next((r for r in student.resumes if r.is_active), None)
        if not active_res and len(student.resumes) > 0:
            active_res = student.resumes[-1]
            
        if active_res:
            has_resume = True
            ext_status = "extracted" if active_res.extracted_text else "not_available"
            res_ctx = AchieverResumeContext(
                filename=active_res.filename,
                mime_type=active_res.content_type,
                file_size=active_res.file_size,
                upload_date=active_res.uploaded_at,
                active_status=active_res.is_active,
                extraction_status=ext_status,
                extracted_text=active_res.extracted_text
            )
            if active_res.extracted_text:
                has_resume_text = True
                
    # 10 & 11 & 12. Evidence
    evidence_list = []
    verified_evidence_count = 0
    unverified_evidence_count = 0
    has_assessment = False
    
    for ev in student.evidence:
        ev_ctx = AchieverEvidenceContext(
            type=ev.evidence_type or ev.source or "unknown",
            status=ev.verification_status or "unverified",
            title=None,
            metadata=ev.extracted_data if ev.extracted_data is not None else {},
            created_at=ev.created_at,
            updated_at=ev.last_synced_at
        )
        evidence_list.append(ev_ctx)
        if ev.verification_status.lower() == "verified":
            verified_evidence_count += 1
        else:
            unverified_evidence_count += 1
            
        if ev.source == "ASSESSMENT":
            has_assessment = True
        elif ev.source == "GITHUB":
            has_github = True
            ext_ctx.github_status = "synced"
        elif ev.source == "LINKEDIN":
            has_linkedin = True
            ext_ctx.linkedin_status = "synced"
        elif ev.source == "PORTFOLIO":
            has_portfolio = True
            ext_ctx.portfolio_status = "synced"
            
    # 13 & 14. Student Skills
    student_skills_db = db.query(StudentSkill).filter(StudentSkill.student_id == student.id).all()
    student_skill_dict = {ss.skill_id: ss for ss in student_skills_db}
    
    skills_ctx_list = []
    for ss in student_skills_db:
        # Determine source status based on SkillEvidence (if any exist)
        skill_evidences = db.query(SkillEvidence).filter(
            SkillEvidence.student_id == student.id, 
            SkillEvidence.skill_id == ss.skill_id
        ).all()
        source_status = "assessed" if skill_evidences else "unverified"
        
        skills_ctx_list.append(AchieverSkillContext(
            skill=SkillResponse.model_validate(ss.skill),
            proficiency_level=ss.proficiency_level,
            source_status=source_status,
            updated_timestamp=ss.last_assessed_at
        ))
        
    # 15. Skill Gaps (Deterministic from required_skills)
    skill_gaps_list = []
    for req in required_skills:
        if not req.skill:
            raise ValueError(f"Data integrity error: Requirement references missing skill (skill_id: {req.skill_id})")
        current_ss = student_skill_dict.get(req.skill_id)
        current_level = current_ss.proficiency_level if current_ss else 0
        
        status_str = "Missing"
        if current_level >= req.required_proficiency_level:
            status_str = "Sufficient"
        elif current_level > 0:
            status_str = "Gap"
            
        skill_gaps_list.append(AchieverSkillGapContext(
            skill=SkillResponse.model_validate(req.skill),
            required_proficiency=req.required_proficiency_level,
            current_proficiency=current_level,
            status=status_str,
            requirement_source=requirement_source
        ))
        
    # Metadata
    metadata_ctx = AchieverMetadataContext(
        context_version="1.0.0",
        generated_at=datetime.now(timezone.utc),
        requirement_source=requirement_source,
        available_evidence_count=len(evidence_list),
        verified_evidence_count=verified_evidence_count,
        unverified_evidence_count=unverified_evidence_count,
        has_resume=has_resume,
        has_resume_text=has_resume_text,
        has_github=has_github,
        has_linkedin=has_linkedin,
        has_portfolio=has_portfolio,
        has_assessment=has_assessment,
        has_target_company=has_target_company,
        has_target_role=has_target_role
    )

    return AchieverContextResponse(
        student=student_ctx,
        academic=acad_ctx,
        professional=prof_ctx,
        target=target_ctx,
        external_profiles=ext_ctx,
        resume=res_ctx,
        evidence=evidence_list,
        skills=skills_ctx_list,
        skill_gaps=skill_gaps_list,
        requirements=req_ctx_list,
        metadata=metadata_ctx
    )
