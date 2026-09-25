import os
import json
import re
import urllib.request
import urllib.error
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api import deps
from app.models import (
    User, Student, StudentAcademicProfile, StudentProfessionalProfile,
    StudentExternalProfiles, StudentResume, StudentEvidence,
    StudentSkill, CareerRoleSkill, TargetCompanyRole, TargetCompanyRoleSkill, TargetCompany
)
from app.schemas.student import (
    StudentResponse, StudentUpdate, GemsPreferenceUpdate,
    AcademicProfileResponse, AcademicProfileUpdate,
    ProfessionalProfileResponse, ProfessionalProfileUpdate,
    ExternalProfilesResponse, ExternalProfilesUpdate,
    StudentResumeResponse, StudentEvidenceResponse
)
from app.schemas.skill import StudentSkillResponse, SkillGapResponse
from app.schemas.achiever import AchieverContextResponse
from app.services.achiever_context import build_achiever_context

router = APIRouter()

STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "storage", "resumes"))
os.makedirs(STORAGE_DIR, exist_ok=True)

def get_or_create_student(db: Session, user: User) -> Student:
    if not user.student:
        new_student = Student(user_id=user.id)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student
    return user.student

# --- Basic & Academic Profiles ---

@router.get("/profile", response_model=StudentResponse)
def get_student_profile(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    return student

@router.put("/profile", response_model=StudentResponse)
def update_student_profile(
    profile_in: StudentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
        
    db.commit()
    db.refresh(student)
    return student

@router.post("/preferences/gems", response_model=StudentResponse)
def update_gems_preferences(
    prefs_in: GemsPreferenceUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    update_data = prefs_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
        
    db.commit()
    db.refresh(student)
    return student

@router.get("/academic", response_model=AcademicProfileResponse)
def get_academic_profile(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    academic = db.query(StudentAcademicProfile).filter(StudentAcademicProfile.student_id == student.id).first()
    if not academic:
        academic = StudentAcademicProfile(student_id=student.id)
        db.add(academic)
        db.commit()
        db.refresh(academic)
    return academic

@router.put("/academic", response_model=AcademicProfileResponse)
def update_academic_profile(
    academic_in: AcademicProfileUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    academic = db.query(StudentAcademicProfile).filter(StudentAcademicProfile.student_id == student.id).first()
    if not academic:
        academic = StudentAcademicProfile(student_id=student.id)
        db.add(academic)
        
    update_data = academic_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(academic, field, value)
        
    db.commit()
    db.refresh(academic)
    return academic

# --- Professional Profile ---

@router.get("/professional", response_model=ProfessionalProfileResponse)
def get_professional_profile(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    prof = db.query(StudentProfessionalProfile).filter(StudentProfessionalProfile.student_id == student.id).first()
    if not prof:
        prof = StudentProfessionalProfile(student_id=student.id)
        db.add(prof)
        db.commit()
        db.refresh(prof)
    return prof

@router.put("/professional", response_model=ProfessionalProfileResponse)
def update_professional_profile(
    prof_in: ProfessionalProfileUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    prof = db.query(StudentProfessionalProfile).filter(StudentProfessionalProfile.student_id == student.id).first()
    if not prof:
        prof = StudentProfessionalProfile(student_id=student.id)
        db.add(prof)
        
    update_data = prof_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prof, field, value)
        
    db.commit()
    db.refresh(prof)
    return prof

# --- External Profiles & Evidence Creation ---

@router.get("/external-profiles", response_model=ExternalProfilesResponse)
def get_external_profiles(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    ext = db.query(StudentExternalProfiles).filter(StudentExternalProfiles.student_id == student.id).first()
    if not ext:
        ext = StudentExternalProfiles(student_id=student.id)
        db.add(ext)
        db.commit()
        db.refresh(ext)

    res = ExternalProfilesResponse.model_validate(ext)
    res.linkedin_sync_status = "Not Synced"
    return res

@router.put("/external-profiles", response_model=ExternalProfilesResponse)
def update_external_profiles(
    ext_in: ExternalProfilesUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    ext = db.query(StudentExternalProfiles).filter(StudentExternalProfiles.student_id == student.id).first()
    if not ext:
        ext = StudentExternalProfiles(student_id=student.id)
        db.add(ext)
        
    update_data = ext_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ext, field, value)
        
    # LinkedIn Evidence Handling (Requirement 6: Store URL, never scrape, status 'Not Synced')
    if ext_in.linkedin_url:
        existing_ev = db.query(StudentEvidence).filter(
            StudentEvidence.student_id == student.id,
            StudentEvidence.source == "LINKEDIN"
        ).first()
        if not existing_ev:
            ev = StudentEvidence(
                student_id=student.id,
                source="LINKEDIN",
                source_url=ext_in.linkedin_url,
                evidence_type="PROFILE_URL",
                extracted_data={"profile_url": ext_in.linkedin_url, "sync_status": "Not Synced", "message": "OAuth integration unavailable"},
                verification_status="not_synced"
            )
            db.add(ev)
        else:
            existing_ev.source_url = ext_in.linkedin_url
            existing_ev.extracted_data = {"profile_url": ext_in.linkedin_url, "sync_status": "Not Synced", "message": "OAuth integration unavailable"}
            existing_ev.verification_status = "not_synced"

    # Portfolio Evidence Handling
    if ext_in.portfolio_url:
        existing_port = db.query(StudentEvidence).filter(
            StudentEvidence.student_id == student.id,
            StudentEvidence.source == "PORTFOLIO"
        ).first()
        if not existing_port:
            ev_port = StudentEvidence(
                student_id=student.id,
                source="PORTFOLIO",
                source_url=ext_in.portfolio_url,
                evidence_type="PORTFOLIO_URL",
                extracted_data={"portfolio_url": ext_in.portfolio_url},
                verification_status="unverified"
            )
            db.add(ev_port)
        else:
            existing_port.source_url = ext_in.portfolio_url
            existing_port.extracted_data = {"portfolio_url": ext_in.portfolio_url}

    db.commit()
    db.refresh(ext)
    
    res = ExternalProfilesResponse.model_validate(ext)
    res.linkedin_sync_status = "Not Synced"
    return res


# --- GitHub API Sync ---

@router.post("/github/sync", response_model=StudentEvidenceResponse)
def sync_github_profile(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Synchronizes public GitHub repositories for student.
    Stores fetched repo information as evidence.
    Does NOT automatically assign verified skill levels to StudentSkill (Requirement 7)."""
    student = get_or_create_student(db, current_user)
    ext = db.query(StudentExternalProfiles).filter(StudentExternalProfiles.student_id == student.id).first()
    if not ext or not ext.github_url:
        raise HTTPException(status_code=400, detail="GitHub profile URL not set")


    # Extract username from github_url (e.g. https://github.com/octocat or octocat)
    url = ext.github_url.strip().rstrip("/")
    username = url.split("/")[-1]
    if not username:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    api_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
    req = urllib.request.Request(api_url, headers={"User-Agent": "Skilly-App"})

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise HTTPException(status_code=404, detail=f"GitHub user '{username}' not found")
        else:
            raise HTTPException(status_code=502, detail=f"GitHub API error: {e.reason}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch GitHub profile: {str(e)}")

    repo_list = []
    languages = set()
    for repo in data:
        lang = repo.get("language")
        if lang:
            languages.add(lang)
        repo_list.append({
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "html_url": repo.get("html_url"),
            "description": repo.get("description"),
            "language": lang,
            "stargazers_count": repo.get("stargazers_count"),
            "updated_at": repo.get("updated_at")
        })

    extracted_info = {
        "username": username,
        "repo_count": len(repo_list),
        "repos": repo_list,
        "languages": list(languages)
    }

    evidence = db.query(StudentEvidence).filter(
        StudentEvidence.student_id == student.id,
        StudentEvidence.source == "GITHUB"
    ).first()

    now = datetime.now(timezone.utc)
    if not evidence:
        evidence = StudentEvidence(
            student_id=student.id,
            source="GITHUB",
            source_url=ext.github_url,
            evidence_type="GITHUB_REPOS",
            extracted_data=extracted_info,
            created_at=now,
            last_synced_at=now,
            verification_status="unverified"
        )
        db.add(evidence)
    else:
        evidence.source_url = ext.github_url
        evidence.extracted_data = extracted_info
        evidence.last_synced_at = now
        evidence.verification_status = "unverified"

    db.commit()
    db.refresh(evidence)
    return evidence

# --- Resume Upload & Private Document Storage ---

@router.post("/resume/upload", response_model=StudentResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Uploads resume to private local storage (Requirement 2, 5).
    Extracts text server-side for PDF, DOCX, DOC, TXT (Requirement 6).
    Saves metadata in PostgreSQL and creates generic StudentEvidence (Requirement 3).
    Does NOT automatically verify skills."""
    student = get_or_create_student(db, current_user)

    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx", ".doc", ".txt"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file format '{ext}'. Allowed formats: PDF, DOC, DOCX, TXT."
        )

    student_storage_dir = os.path.join(STORAGE_DIR, str(student.id))
    os.makedirs(student_storage_dir, exist_ok=True)

    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    safe_filename = f"resume_{timestamp_str}_{re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename)}"
    file_path = os.path.join(student_storage_dir, safe_filename)

    contents = await file.read()
    file_size = len(contents)
    
    if file_size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds maximum limit of 10 MB."
        )

    with open(file_path, "wb") as f:
        f.write(contents)

    # Server-side text extraction
    extracted_text = None
    try:
        if ext == ".pdf":
            import pypdf
            reader = pypdf.PdfReader(file_path)
            pages_text = [page.extract_text() or "" for page in reader.pages]
            extracted_text = "\n".join(pages_text).strip()
        elif ext in [".docx", ".doc"]:
            import docx
            doc = docx.Document(file_path)
            paragraphs_text = [p.text for p in doc.paragraphs if p.text]
            extracted_text = "\n".join(paragraphs_text).strip()
        elif ext == ".txt":
            extracted_text = contents.decode("utf-8", errors="ignore").strip()
    except Exception as ex:
        extracted_text = None

    # Deactivate older active resumes
    db.query(StudentResume).filter(
        StudentResume.student_id == student.id,
        StudentResume.is_active == True
    ).update({"is_active": False})

    resume = StudentResume(
        student_id=student.id,
        filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        content_type=file.content_type or "application/octet-stream",
        uploaded_at=datetime.now(timezone.utc),
        is_active=True,
        extracted_text=extracted_text
    )
    db.add(resume)
    db.flush()

    # Generic evidence record (Requirement 3: Marked UNVERIFIED)
    ev = StudentEvidence(
        student_id=student.id,
        source="RESUME",
        evidence_type="RESUME_UPLOAD",
        extracted_data={
            "resume_id": resume.id, 
            "filename": file.filename, 
            "file_size": file_size,
            "has_text": bool(extracted_text)
        },
        created_at=datetime.now(timezone.utc),
        verification_status="unverified"
    )
    db.add(ev)

    db.commit()
    db.refresh(resume)
    return resume


@router.get("/resume/active", response_model=Optional[StudentResumeResponse])
def get_active_resume(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    resume = db.query(StudentResume).filter(
        StudentResume.student_id == student.id,
        StudentResume.is_active == True
    ).order_by(StudentResume.uploaded_at.desc()).first()
    return resume

@router.get("/resume/{resume_id}/download")
def download_resume(
    resume_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Authenticated endpoint to securely download student resume (Requirement 2, 5)."""
    student = get_or_create_student(db, current_user)
    resume = db.query(StudentResume).filter(
        StudentResume.id == resume_id,
        StudentResume.student_id == student.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume file not found")
    if not os.path.exists(resume.file_path):
        raise HTTPException(status_code=404, detail="Physical file missing on server")

    return FileResponse(
        path=resume.file_path,
        filename=resume.filename,
        media_type=resume.content_type
    )

# --- Generic Evidence Timeline ---

@router.get("/evidence", response_model=List[StudentEvidenceResponse])
def get_student_evidence(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    return db.query(StudentEvidence).filter(StudentEvidence.student_id == student.id).order_by(StudentEvidence.created_at.desc()).all()

# --- Student Skills & Skill Gaps ---

@router.get("/skills", response_model=List[StudentSkillResponse])
def get_student_skills(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    student = get_or_create_student(db, current_user)
    return db.query(StudentSkill).filter(StudentSkill.student_id == student.id).all()

@router.get("/skill-gaps", response_model=List[SkillGapResponse])
def get_skill_gaps(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Calculates skill gaps. Checks for target company-specific requirements (Requirement 8).
    If unavailable, falls back seamlessly to role-based career_role_skills data."""
    student = get_or_create_student(db, current_user)
    career_goal = student.career_goal
    if not career_goal or not career_goal.career_role_id:
        return []

    target_company_id = career_goal.target_company_id
    career_role_id = career_goal.career_role_id
    
    required_skills = []
    requirement_source = "role_fallback"
    company_name = None

    if target_company_id:
        company = db.query(TargetCompany).filter(TargetCompany.id == target_company_id).first()
        if company:
            company_name = company.name

        # Look up company-role mapping
        comp_role = db.query(TargetCompanyRole).filter(
            TargetCompanyRole.company_id == target_company_id,
            TargetCompanyRole.career_role_id == career_role_id
        ).first()

        if comp_role:
            comp_skills = db.query(TargetCompanyRoleSkill).filter(
                TargetCompanyRoleSkill.target_company_role_id == comp_role.id
            ).all()
            if comp_skills:
                required_skills = comp_skills
                requirement_source = "company_specific"

    # Fallback to standard role skills if company-specific skills not found (Requirement 8)
    if not required_skills:
        required_skills = db.query(CareerRoleSkill).filter(
            CareerRoleSkill.career_role_id == career_role_id
        ).all()
        requirement_source = "role_fallback"

    student_skills = db.query(StudentSkill).filter(StudentSkill.student_id == student.id).all()
    student_skill_dict = {ss.skill_id: ss for ss in student_skills}

    gaps = []
    for req in required_skills:
        current_ss = student_skill_dict.get(req.skill_id)
        current_level = current_ss.proficiency_level if current_ss else 0
        current_score = current_ss.score if current_ss else 0.0

        status_str = "Missing"
        if current_level >= req.required_proficiency_level:
            status_str = "Sufficient"
        elif current_level > 0:
            status_str = "Gap"

        gaps.append(
            SkillGapResponse(
                skill=req.skill,
                required_level=req.required_proficiency_level,
                current_level=current_level,
                current_score=current_score,
                gap_status=status_str,
                requirement_source=requirement_source,
                target_company_name=company_name if requirement_source == "company_specific" else None
            )
        )
    return gaps

# --- Achiever AI Context ---

@router.get("/achiever/context", response_model=AchieverContextResponse)
def get_achiever_context(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Returns the read-only, deterministic Achiever Context for the authenticated student.
    Collects profiles, evidence, requirements, and skill gaps without mutating data.
    """
    student = get_or_create_student(db, current_user)
    return build_achiever_context(db, student)


from app.schemas.achiever import AchieverPriorityResponse
from app.services.achiever_priority import build_priorities

@router.get("/achiever/priorities", response_model=AchieverPriorityResponse)
def get_achiever_priorities(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Returns the deterministic Achiever Priority Context for the authenticated student.
    Analyzes evidence and assigns a priority to each skill gap.
    """
    student = get_or_create_student(db, current_user)
    context = build_achiever_context(db, student)
    return build_priorities(db, student, context)


from app.schemas.knowledge import AchieverResourcesResponse, SkillResourceGroup
from app.services.knowledge_retrieval import retrieve_resources_for_skill
from app.services.knowledge_reranker import knowledge_reranker

@router.get("/achiever/resources", response_model=AchieverResourcesResponse)
def get_achiever_resources(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Retrieves recommended learning resources based on prioritized skill gaps.
    """
    student = get_or_create_student(db, current_user)
    context = build_achiever_context(db, student)
    priorities = build_priorities(db, student, context)
    
    target_dict = {
        "company": priorities.target.target_company.name if priorities.target.target_company else "None",
        "role": priorities.target.target_role.name if priorities.target.target_role else "None"
    }

    groups = []
    
    # Process only gaps that actually need resources (i.e. not Sufficient)
    # Priority engine already filters out Sufficient if they aren't gaps, but just to be sure
    for gap in priorities.prioritized_gaps:
        if gap.gap_status == "Sufficient":
            continue
            
        # 1. Determine ideal difficulty based on current proficiency
        # Current proficiency mapping: 0=beginner, 1-2=beginner/intermediate, 3=intermediate, 4-5=advanced
        difficulty = "beginner"
        if gap.current_proficiency >= 3:
            difficulty = "advanced"
        elif gap.current_proficiency >= 1:
            difficulty = "intermediate"

        # 2. Formulate a search query
        # We can use the skill name, target role, and gap status
        query = f"Learn {gap.skill.name} for {target_dict['role']}"

        # 3. Retrieve from Vector DB
        raw_resources = retrieve_resources_for_skill(
            db=db,
            query=query,
            skill_id=gap.skill.id,
            difficulty=difficulty,
            top_k=3
        )
        
        # If no resources found for specific difficulty, widen search
        if not raw_resources:
             raw_resources = retrieve_resources_for_skill(
                 db=db,
                 query=query,
                 skill_id=gap.skill.id,
                 difficulty=None,
                 top_k=3
             )

        # 4. Rerank
        final_resources = knowledge_reranker.rerank(query, raw_resources)

        groups.append(
            SkillResourceGroup(
                skill_id=gap.skill.id,
                skill_name=gap.skill.name,
                priority=gap.priority,
                resources=final_resources
            )
        )

    return AchieverResourcesResponse(
        student_id=student.id,
        target=target_dict,
        resources=groups
    )

from app.schemas.roadmap import RoadmapResponse
from app.services.achiever_roadmap import get_student_roadmap, generate_student_roadmap

@router.get("/achiever/roadmap", response_model=Optional[RoadmapResponse])
def get_roadmap_endpoint(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Retrieves the personalized roadmap for the current target role."""
    student = get_or_create_student(db, current_user)
    return get_student_roadmap(db, student)

@router.post("/achiever/roadmap/generate", response_model=RoadmapResponse)
def generate_roadmap_endpoint(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Deterministically generates a personalized roadmap using Achiever AI Priorities and RAG resources."""
    student = get_or_create_student(db, current_user)
    # Target role check
    context = build_achiever_context(db, student)
    if not context.target.target_role:
        raise HTTPException(status_code=400, detail="Must set a target role before generating a roadmap.")
        
    return generate_student_roadmap(db, student)

from app.schemas.gems import GemsDailyPlanResponse, GemsTaskResponse, HelpContextResponse
from app.services.gems_daily_plan import get_or_generate_daily_plan, update_task_status, get_help_context
from pydantic import BaseModel

class TaskCompletionRequest(BaseModel):
    note: Optional[str] = None

@router.get("/gems/today", response_model=Optional[GemsDailyPlanResponse])
def get_gems_today_endpoint(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    student = get_or_create_student(db, current_user)
    return get_or_generate_daily_plan(db, student)

@router.post("/gems/tasks/{task_id}/start", response_model=GemsTaskResponse)
def start_gems_task_endpoint(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    student = get_or_create_student(db, current_user)
    return update_task_status(db, student, task_id, "in_progress")

@router.post("/gems/tasks/{task_id}/complete", response_model=GemsTaskResponse)
def complete_gems_task_endpoint(
    task_id: int,
    req: TaskCompletionRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    student = get_or_create_student(db, current_user)
    return update_task_status(db, student, task_id, "completed", req.note)

@router.post("/gems/tasks/{task_id}/skip", response_model=GemsTaskResponse)
def skip_gems_task_endpoint(
    task_id: int,
    req: TaskCompletionRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    student = get_or_create_student(db, current_user)
    return update_task_status(db, student, task_id, "skipped", req.note)

@router.post("/gems/tasks/{task_id}/reschedule", response_model=GemsTaskResponse)
def reschedule_gems_task_endpoint(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    student = get_or_create_student(db, current_user)
    return update_task_status(db, student, task_id, "rescheduled")

@router.get("/gems/tasks/{task_id}/help", response_model=HelpContextResponse)
def help_gems_task_endpoint(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    student = get_or_create_student(db, current_user)
    return get_help_context(db, student, task_id)

from app.schemas.student import GemsPreferenceUpdate

@router.post("/preferences/gems")
def update_gems_preferences(
    req: GemsPreferenceUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    student = get_or_create_student(db, current_user)
    student.gems_enabled = req.gems_enabled
    student.gems_reminder_enabled = req.gems_reminder_enabled
    student.gems_reminder_time = req.gems_reminder_time
    db.commit()
    db.refresh(student)
    return {"message": "Preferences updated successfully"}
