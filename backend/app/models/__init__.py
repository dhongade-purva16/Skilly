from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    user_type = Column(String, default="student") # student, hr
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="user", uselist=False)
    hr_profile = relationship("HRProfile", back_populates="user", uselist=False)
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    gems_enabled = Column(Boolean, default=False)
    gems_reminder_enabled = Column(Boolean, default=False)
    gems_reminder_time = Column(String, nullable=True)
    
    user = relationship("User", back_populates="student")
    academic_profile = relationship("StudentAcademicProfile", back_populates="student", uselist=False)
    professional_profile = relationship("StudentProfessionalProfile", back_populates="student", uselist=False)
    external_profiles = relationship("StudentExternalProfiles", back_populates="student", uselist=False)
    career_goal = relationship("StudentCareerGoal", back_populates="student", uselist=False)
    skills = relationship("StudentSkill", back_populates="student")
    resumes = relationship("StudentResume", back_populates="student")
    evidence = relationship("StudentEvidence", back_populates="student")

class StudentAcademicProfile(Base):
    __tablename__ = "student_academic_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    degree = Column(String, nullable=True)
    branch = Column(String, nullable=True)
    academic_year = Column(String, nullable=True)
    graduation_year = Column(Integer, nullable=True)
    
    student = relationship("Student", back_populates="academic_profile")

class CareerRole(Base):
    __tablename__ = "career_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    required_skills = relationship("CareerRoleSkill", back_populates="career_role")

class TargetCompany(Base):
    __tablename__ = "target_companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    normalized_name = Column(String, unique=True, index=True)
    website = Column(String, nullable=True)
    description = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    source = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TargetCompanyRole(Base):
    __tablename__ = "target_company_roles"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("target_companies.id"))
    career_role_id = Column(Integer, ForeignKey("career_roles.id"))
    
    company = relationship("TargetCompany")
    career_role = relationship("CareerRole")
    company_skills = relationship("TargetCompanyRoleSkill", back_populates="target_company_role")

class TargetCompanyRoleSkill(Base):
    __tablename__ = "target_company_role_skills"

    id = Column(Integer, primary_key=True, index=True)
    target_company_role_id = Column(Integer, ForeignKey("target_company_roles.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    required_proficiency_level = Column(Integer) # 1 to 5

    target_company_role = relationship("TargetCompanyRole", back_populates="company_skills")
    skill = relationship("Skill")

class StudentCareerGoal(Base):
    __tablename__ = "student_career_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    career_role_id = Column(Integer, ForeignKey("career_roles.id"))
    target_company_id = Column(Integer, ForeignKey("target_companies.id"), nullable=True)
    
    student = relationship("Student", back_populates="career_goal")
    career_role = relationship("CareerRole")
    target_company = relationship("TargetCompany")

class StudentProfessionalProfile(Base):
    __tablename__ = "student_professional_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    headline = Column(String, nullable=True)
    current_status = Column(String, nullable=True) # e.g. "Student", "Intern", "Fresher"
    experience_level = Column(String, nullable=True)
    years_of_experience = Column(Float, nullable=True)
    professional_summary = Column(String, nullable=True)
    work_domain = Column(String, nullable=True)
    
    student = relationship("Student", back_populates="professional_profile")

class StudentExternalProfiles(Base):
    __tablename__ = "student_external_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    portfolio_url = Column(String, nullable=True)
    
    student = relationship("Student", back_populates="external_profiles")

class StudentResume(Base):
    __tablename__ = "student_resumes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    extracted_text = Column(String, nullable=True)

    student = relationship("Student", back_populates="resumes")

class StudentEvidence(Base):
    __tablename__ = "student_evidence"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    source = Column(String) # RESUME, GITHUB, LINKEDIN, PORTFOLIO, ASSESSMENT
    source_url = Column(String, nullable=True)
    evidence_type = Column(String) 
    extracted_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    confidence = Column(Float, nullable=True)
    verification_status = Column(String, default="unverified")
    
    student = relationship("Student", back_populates="evidence")

class SkillCategory(Base):
    __tablename__ = "skill_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category_id = Column(Integer, ForeignKey("skill_categories.id"))
    
    category = relationship("SkillCategory")

class CareerRoleSkill(Base):
    __tablename__ = "career_role_skills"

    id = Column(Integer, primary_key=True, index=True)
    career_role_id = Column(Integer, ForeignKey("career_roles.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    required_proficiency_level = Column(Integer) # 1 to 5
    
    career_role = relationship("CareerRole", back_populates="required_skills")
    skill = relationship("Skill")

class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    proficiency_level = Column(Integer, default=0)
    score = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    last_assessed_at = Column(DateTime(timezone=True), nullable=True)
    
    student = relationship("Student", back_populates="skills")
    skill = relationship("Skill")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True) # made nullable for job-level assessments
    target_company_id = Column(Integer, ForeignKey("target_companies.id"), nullable=True)
    company_job_id = Column(Integer, ForeignKey("company_jobs.id", ondelete="CASCADE"), nullable=True)
    total_marks = Column(Integer, nullable=True)
    passing_criteria = Column(Float, nullable=True)
    
    skill = relationship("Skill")
    target_company = relationship("TargetCompany")
    company_job = relationship("CompanyJob", back_populates="assessments")
    questions = relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    question_text = Column(String)
    options = Column(JSON) # e.g. ["A", "B", "C", "D"]
    correct_option_index = Column(Integer)
    difficulty = Column(Integer, default=1)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True) # mapped to specific skill
    
    assessment = relationship("Assessment", back_populates="questions")
    skill = relationship("Skill")

class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"))
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    score = Column(Float, nullable=True) # kept for backward compatibility
    overall_score = Column(Float, nullable=True)
    skill_wise_scores = Column(JSON, nullable=True)
    
    student = relationship("Student")
    assessment = relationship("Assessment")
    answers = relationship("AssessmentAnswer", back_populates="attempt")

class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("assessment_attempts.id"))
    question_id = Column(Integer, ForeignKey("assessment_questions.id"))
    selected_option_index = Column(Integer)
    is_correct = Column(Boolean, default=False)
    
    attempt = relationship("AssessmentAttempt", back_populates="answers")
    question = relationship("AssessmentQuestion")

class SkillEvidence(Base):
    __tablename__ = "skill_evidence"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    source_type = Column(String) # e.g. "Assessment", "Project"
    source_id = Column(Integer, nullable=True) # e.g. AssessmentAttempt.id
    evidence_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    student = relationship("Student")
    skill = relationship("Skill")

from pgvector.sqlalchemy import Vector

class KnowledgeResource(Base):
    __tablename__ = "knowledge_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    resource_type = Column(String, index=True) # course, tutorial, documentation, etc.
    provider = Column(String, index=True)
    source_url = Column(String)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True, index=True)
    difficulty = Column(String, nullable=True) # beginner, intermediate, advanced
    estimated_duration = Column(String, nullable=True)
    language = Column(String, default="en")
    trust_status = Column(String, default="pending", index=True) # pending, approved, rejected
    source_type = Column(String, nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    metadata_json = Column(JSON, nullable=True)

    skill = relationship("Skill")
    chunks = relationship("KnowledgeChunk", back_populates="resource", cascade="all, delete-orphan")

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True, index=True)
    knowledge_resource_id = Column(Integer, ForeignKey("knowledge_resources.id", ondelete="CASCADE"), index=True)
    chunk_index = Column(Integer)
    content = Column(String)
    embedding = Column(Vector(384)) # Using all-MiniLM-L6-v2 which has 384 dimensions
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resource = relationship("KnowledgeResource", back_populates="chunks")

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    target_company_id = Column(Integer, ForeignKey("target_companies.id"), nullable=True)
    target_role_id = Column(Integer, ForeignKey("career_roles.id"), nullable=True)
    status = Column(String, default="not_started")
    title = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    student = relationship("Student")
    target_company = relationship("TargetCompany")
    target_role = relationship("CareerRole")
    steps = relationship("RoadmapStep", back_populates="roadmap", cascade="all, delete-orphan")

class RoadmapStep(Base):
    __tablename__ = "roadmap_steps"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), index=True)
    step_order = Column(Integer)
    title = Column(String)
    objective = Column(String)
    description = Column(String, nullable=True)
    priority = Column(String) # HIGH, MEDIUM, LOW
    estimated_duration = Column(String, nullable=True)
    status = Column(String, default="not_started") # not_started, in_progress, completed
    resource_references = Column(JSON, nullable=True) # stores selected KnowledgeResource metadata
    practice_task = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    roadmap = relationship("Roadmap", back_populates="steps")
    skill = relationship("Skill")

from sqlalchemy import Date

class GemsDailyPlan(Base):
    __tablename__ = "gems_daily_plans"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=True, index=True)
    plan_date = Column(Date, index=True)
    status = Column(String, default="active") # active, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    student = relationship("Student")
    roadmap = relationship("Roadmap")
    tasks = relationship("GemsTask", back_populates="daily_plan", cascade="all, delete-orphan")

class GemsTask(Base):
    __tablename__ = "gems_tasks"

    id = Column(Integer, primary_key=True, index=True)
    daily_plan_id = Column(Integer, ForeignKey("gems_daily_plans.id", ondelete="CASCADE"), index=True)
    roadmap_step_id = Column(Integer, ForeignKey("roadmap_steps.id"), nullable=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    title = Column(String)
    description = Column(String, nullable=True)
    task_type = Column(String) # learning, practice, project, review
    estimated_minutes = Column(Integer, default=30)
    priority = Column(String, default="MEDIUM")
    scheduled_date = Column(Date, index=True)
    status = Column(String, default="not_started") # not_started, in_progress, completed, skipped, rescheduled
    order_index = Column(Integer, default=0)
    resource_references = Column(JSON, nullable=True)
    completion_note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    daily_plan = relationship("GemsDailyPlan", back_populates="tasks")
    roadmap_step = relationship("RoadmapStep")
    skill = relationship("Skill")

class HRProfile(Base):
    __tablename__ = "hr_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    company_id = Column(Integer, ForeignKey("target_companies.id"))

    user = relationship("User", back_populates="hr_profile")
    company = relationship("TargetCompany")

class CompanyJob(Base):
    __tablename__ = "company_jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("target_companies.id"))
    title = Column(String)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)
    work_mode = Column(String, nullable=True) # REMOTE, HYBRID, ONSITE
    eligibility = Column(String, nullable=True)
    experience_requirement = Column(String, nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    assessment_required = Column(Boolean, default=True)
    status = Column(String, default="active") # active, closed, draft
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("TargetCompany")
    skills = relationship("CompanyJobSkill", back_populates="company_job", cascade="all, delete-orphan")
    applications = relationship("JobApplication", back_populates="company_job", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="company_job", cascade="all, delete-orphan")

class CompanyJobSkill(Base):
    __tablename__ = "company_job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("company_jobs.id", ondelete="CASCADE"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    required_level = Column(Integer, default=1)
    priority = Column(String, default="MEDIUM")

    company_job = relationship("CompanyJob", back_populates="skills")
    skill = relationship("Skill")

class JobApplication(Base):
    __tablename__ = "job_applications"
    __table_args__ = (UniqueConstraint('job_id', 'student_id', name='uix_job_student'),)

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("company_jobs.id", ondelete="CASCADE"))
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    status = Column(String, default="applied") # applied, assessment_pending, assessment_completed, shortlisted, rejected
    assessment_attempt_id = Column(Integer, ForeignKey("assessment_attempts.id", ondelete="SET NULL"), nullable=True)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company_job = relationship("CompanyJob", back_populates="applications")
    student = relationship("Student")
    assessment_attempt = relationship("AssessmentAttempt")
