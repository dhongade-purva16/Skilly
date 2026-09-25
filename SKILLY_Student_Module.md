# SKILLY — Student Module

## Module Overview

The Student Module is the first major implementation area of SKILLY.

It will be developed independently before the College and Industry modules are designed.

**Important scope rule:** College–Student and Industry–Student relationships are intentionally NOT assumed or implemented at this stage because their feature sets and workflows have not yet been defined.

The Student Module contains seven integrated features:

1. Student Profile & Career Goal
2. Skill Assessment & Skill Profile
3. Achiever AI + GEMS
4. Internship Management & Tracking
5. Training, Workshops, Mentorship & Student Engagement
6. Secure Document Management
7. Career Growth & Verified Profile

---

# Student Module Architecture

```text
                         STUDENT MODULE
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        PHASE 1            PHASE 2          PHASE 3
        FOUNDATION         DEVELOPMENT       CAREER
              │                │                │
              ▼                ▼                ▼
         Profile           Achiever AI      Internship
              │                │                │
         Assessment           GEMS           Documents
              │                │                │
        Skill Profile       Training         Verified
              │              Workshops        Profile
         Skill Gap          Mentorship          │
              │            Competitions         │
              │             Community           │
              └────────────────┬────────────────┘
                               ▼
                     Student Career Loop
```

---

# Three-Phase Implementation Plan

## Phase 1 — Student Foundation & Skill Intelligence

### Objective

Establish the student's identity, academic/career direction, assessment results, evidence-based skill profile and skill gaps.

### Features

- Student Profile & Career Goal
- Skill Assessment & Skill Profile
- Initial Achiever AI Skill Gap Foundation

### Flow

```text
Registration
    ↓
Student Profile
    ↓
Academic Profile
    ↓
Career Interests
    ↓
Target Career
    ↓
Required Role Skills
    ↓
Assessment
    ↓
Evaluation
    ↓
Evidence-Based Skill Profile
    ↓
Skill Gap Analysis
    ↓
Priority Skill Gaps
```

### Phase 1 Output

```text
Student
  ↓
Target Career
  ↓
Current Skills
  ↓
Skill Levels + Confidence
  ↓
Required Role Skills
  ↓
Skill Gaps
  ↓
Priority Gaps
```

---

# Phase 2 — AI Development & Student Engagement

## Objective

Use the Phase 1 skill state to create personalized development plans and help students execute them.

### Features

- Achiever AI + GEMS
- Training
- Workshops
- Mentorship
- Community
- Competitions / Hackathons
- Achievements / Engagement

### Achiever AI Flow

```text
Skill Profile
    +
Target Career
    +
Skill Gap
    ↓
Skill Dependency Graph
    ↓
Hybrid Retrieval
    ↓
Vector Semantic Search
    ↓
Reranking
    ↓
RAG Context
    ↓
LLM Personalization
    ↓
Personalized Roadmap
    ↓
GEMS
    ↓
Daily Tasks
    ↓
Progress
```

### GEMS

GEMS is an internal component of Achiever AI.

```text
Personalized Roadmap
       ↓
Goals
       ↓
Milestones
       ↓
Tasks
       ↓
Task Dependencies
       ↓
Daily Scheduling
       ↓
Reminder
       ↓
Student Completion
       ↓
Progress Update
```

### Phase 2 Student Development Loop

```text
Skill Gap
    ↓
Roadmap
    ↓
Learning
    ↓
Practice
    ↓
Training / Workshops
    ↓
Mentorship
    ↓
Competitions
    ↓
New Evidence
    ↓
Updated Progress
```

---

# Phase 3 — Career Execution & Verified Profile

## Objective

Convert student development activity into career opportunities and proof-backed career identity.

### Features

- Internship Management & Tracking
- Secure Document Management
- Career Growth & Verified Profile

### Internship Flow

```text
Skills
  +
Career Goal
  +
Skill Gap
  +
Projects
  +
Learning Progress
       ↓
Internship Matching
       ↓
Semantic Search
       ↓
Eligibility
       ↓
Relevant Opportunities
       ↓
Application
       ↓
Tracking
       ↓
Internship Experience
       ↓
Evidence
```

### Document Flow

```text
Document
    ↓
Upload
    ↓
Validation
    ↓
Private Storage
    ↓
Verification Status
    ↓
Evidence
```

### Career Growth Flow

```text
Assessment
    +
Projects
    +
Training
    +
Certificates
    +
Internships
    +
Competitions
    +
Achievements
       ↓
Evidence Engine
       ↓
Verified Skills
       ↓
Skill Passport
       ↓
Portfolio
       ↓
Resume
       ↓
Career Profile
```

---

# Feature 1 — Student Profile & Career Goal

## Purpose

Create the student's structured identity and career direction.

## Components

### Registration

- Account creation
- Authentication
- Basic identity

### Personal Profile

- Name
- Contact information
- Profile information
- Basic preferences

### Academic Profile

- Institution information
- Degree/program
- Branch/discipline
- Academic year
- Graduation information

### Career Interests

- Areas of interest
- Preferred domains
- Preferred industries
- Career preferences

### Target Career

- Target role
- Target domain
- Career objective

## Technical Foundation

```text
React
    ↓
FastAPI
    ↓
Pydantic Validation
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

## Core Entities

```text
users
students
student_academic_profiles
career_roles
student_career_goals
```

---

# Feature 2 — Skill Assessment & Skill Profile

## Purpose

Measure actual student capability and convert assessment results into an evidence-based skill profile.

## Assessment Types

- Technical
- Soft Skill
- Aptitude
- Role-specific
- Scenario-based
- Coding/practical assessments where applicable

## Assessment Flow

```text
Target Career
    ↓
Required Skills
    ↓
Assessment Selection
    ↓
Questions
    ↓
Student Attempt
    ↓
Evaluation
    ↓
Skill-wise Scores
    ↓
Skill Profile
```

## Evidence-Based Skill Model

A skill should not be represented only as:

```text
Python = Advanced
```

Instead:

```text
Skill: Python

Level: Intermediate

Evidence:
 ├── Assessment Score
 ├── Projects
 ├── Certification
 ├── Internship
 └── Industry Evaluation when such functionality is later defined

Confidence: 0.86
```

The exact evidence sources available during Student-only implementation must come from implemented Student features. Future College/Industry evidence should not be assumed now.

## Advanced Assessment

Future adaptive assessment can use:

- Item Response Theory (IRT)
- Computerized Adaptive Testing (CAT)
- Difficulty-based question selection

## Core Entities

```text
skills
skill_categories
assessments
assessment_questions
assessment_options
assessment_attempts
assessment_answers
student_skills
skill_evidence
```

---

# Feature 3 — Achiever AI + GEMS

## Purpose

Convert verified skill state and skill gaps into a personalized, evidence-grounded development roadmap.

## Important Principle

Achiever AI must NOT work as:

```text
Student Profile → LLM → Roadmap
```

It should work as:

```text
Profile
   ↓
Assessment
   ↓
Skill Profile
   ↓
Target Role Requirements
   ↓
Skill Gap
   ↓
Skill Dependencies
   ↓
Semantic Retrieval
   ↓
RAG
   ↓
LLM Personalization
   ↓
Roadmap
   ↓
GEMS
```

## Skill Gap Engine

Basic concept:

```text
Gap = Required Skill Level - Current Skill Level
```

Priority should consider:

```text
Gap Severity
+
Role Importance
+
Skill Dependency
+
Career Relevance
+
Assessment Confidence
```

The exact weights should be configurable in backend logic.

## Skill Dependency Graph

Example:

```text
Python
   ↓
FastAPI
   ↓
REST API
   ↓
Authentication
   ↓
Backend Project
   ↓
Docker
```

Initial implementation can use:

- PostgreSQL for relationships
- NetworkX for graph computation

Neo4j can be considered later if graph requirements justify it.

## RAG Pipeline

```text
Skill Gap
   ↓
Query Construction
   ↓
Metadata Filtering
   ↓
Embedding
   ↓
Vector Search
   ↓
Top-K Results
   ↓
Reranking
   ↓
Trusted Context
   ↓
LLM
```

## Vector Search

Initial recommendation:

**PostgreSQL + pgvector**

Potential future alternatives:

- Qdrant
- Weaviate
- Pinecone

## RAG Knowledge Sources

The Student implementation should use trusted/canonical platform data such as:

```text
Career Role Requirements
Learning Resources
Courses
Documentation
Projects
Practice Problems
Certifications
Interview Topics
Soft Skill Resources
Training Content
```

Industry-specific requirements should only be added after the Industry module defines and supplies them.

## Resource Metadata

```json
{
  "skill": "Docker",
  "level": "Intermediate",
  "role": "Backend Developer",
  "resource_type": "course",
  "difficulty": "medium",
  "duration_hours": 12,
  "source": "verified"
}
```

## Hybrid Retrieval

```text
Metadata Filtering
        +
Vector Similarity
        +
Reranking
```

## LLM Personalization

LLM receives:

```text
Student Skills
Target Career
Priority Gaps
Skill Dependencies
Available Time
Retrieved Resources
```

It generates a structured roadmap rather than uncontrolled free text.

## Roadmap Output

```json
{
  "roadmap": [
    {
      "week": 1,
      "skill": "SQL",
      "objective": "Intermediate SQL",
      "resources": ["resource_123"],
      "practice": ["problem_21"]
    }
  ]
}
```

## GEMS Data

```text
roadmaps
roadmap_milestones
roadmap_tasks
student_task_progress
```

---

# Feature 4 — Internship Management & Tracking

## Purpose

Allow students to discover relevant internships, apply, track applications and maintain internship progress.

## Student-Side Flow

```text
Student Skills
     +
Career Goal
     +
Skill Gap
     +
Projects
     +
Learning Progress
     ↓
Matching
     ↓
Relevant Internship
     ↓
Eligibility
     ↓
Apply
     ↓
Track
     ↓
Internship
     ↓
Completion
     ↓
Evidence
```

## Important Scope Boundary

At Student Module stage:

- Build the student-side internship experience.
- Build the matching/application/tracking foundation.
- Do NOT assume how future Industry organizations will publish opportunities.
- Do NOT assume College placement workflows.
- Do NOT implement College/Industry-specific relationships until those modules are designed.

The opportunity provider model should remain extensible.

## Semantic Matching

Potential inputs:

```text
Internship Description
Student Career Goal
Student Skills
Student Projects
Verified Profile
```

Pipeline:

```text
Embedding
    ↓
pgvector
    ↓
Semantic Similarity
    ↓
Skill Matching
    ↓
Eligibility Filtering
    ↓
Ranking
```

Mandatory eligibility conditions should remain deterministic.

## Application Lifecycle

```text
APPLIED
   ↓
SHORTLISTED
   ↓
INTERVIEW
   ↓
SELECTED
   ↓
JOINED
   ↓
IN_PROGRESS
   ↓
COMPLETED
```

## Core Entities

```text
internship_opportunities
opportunity_skills
opportunity_eligibility
internship_applications
application_status_history
internship_enrollments
internship_tasks
internship_evaluations
```

The ownership/provider relationships for opportunities will be finalized after College and Industry modules are designed.

---

# Feature 5 — Training, Workshops, Mentorship & Student Engagement

This is one integrated Student feature containing:

- Training
- Workshops
- Mentorship
- Community
- Contributions
- Competitions/Hackathons
- Achievements

---

## Training Recommendation

```text
Skill Gap
    ↓
Required Skill
    ↓
Metadata Filtering
    ↓
Vector Search
    ↓
Reranking
    ↓
Relevant Training
```

---

## Workshops

```text
Workshop
   ↓
View
   ↓
Eligibility
   ↓
Register
   ↓
Attend
   ↓
Completion
   ↓
Evidence
```

---

## Open Mentorship

Any qualified person can register to provide mentorship.

Potential mentors:

- Faculty
- Successful seniors
- Alumni
- Developers
- Industry professionals
- Researchers
- Entrepreneurs
- Domain experts
- Other qualified mentors

### Mentor Registration

```text
Potential Mentor
      ↓
Register as Mentor
      ↓
Mentor Profile
      ↓
Expertise
      ↓
Experience
      ↓
Availability
      ↓
Verification where required
      ↓
Mentor Listed
```

Important:

```text
Registered ≠ Verified
```

### Mentor Matching

```text
Student Career Goal
+
Skill Gap
+
Interests
      ↓
Mentor Search / Semantic Matching
      ↓
Relevant Mentors
      ↓
Request
      ↓
Accept / Decline
      ↓
Connection
      ↓
Sessions
      ↓
Feedback
```

### Core Mentor Entities

```text
mentors
mentor_expertise
mentor_availability
mentor_verifications
mentorship_requests
mentorship_connections
mentorship_sessions
mentor_feedback
```

Future College/Industry relationships should not be assumed at this stage.

---

## Community

Student engagement can include:

- Discussions
- Contributions
- Knowledge/resource sharing
- Peer support
- Community participation

---

## Competitions / Hackathons

```text
Competition
    ↓
Eligibility
    ↓
Register
    ↓
Participate
    ↓
Submit
    ↓
Result
    ↓
Achievement
```

---

# Feature 6 — Secure Document Management

## Purpose

Provide a secure private document vault for Student data.

## Documents

Examples:

```text
Resume
Academic Documents
Marksheets
Certificates
Training Certificates
Internship Documents
Competition Certificates
Project Documents
Other Career Evidence
```

## Architecture

```text
React
  ↓
FastAPI
  ↓
Authentication / Authorization
  ↓
File Validation
  ↓
Object Storage
  ↓
Metadata in PostgreSQL
```

## Storage

Possible technologies:

- AWS S3
- Cloudflare R2
- Supabase Storage
- Azure Blob

## Metadata

```text
documents
 ├── id
 ├── student_id
 ├── document_type
 ├── storage_key
 ├── file_name
 ├── mime_type
 ├── file_size
 ├── uploaded_at
 └── verification_status
```

Actual files should not be stored directly inside PostgreSQL.

## Secure Download

```text
JWT
 ↓
Ownership Check
 ↓
Authorization
 ↓
Signed Temporary URL
 ↓
Private File Access
```

## Document Intelligence

Optional processing:

```text
Upload
 ↓
Virus Scan
 ↓
OCR
 ↓
Document Classification
 ↓
Information Extraction
 ↓
Verification
 ↓
Evidence
```

Technologies can include:

- ClamAV
- Tesseract / OCR service
- Structured LLM extraction

Extracted information must not automatically become verified evidence.

---

# Feature 7 — Career Growth & Verified Profile

## Purpose

Turn Student activities and evidence into a verified career identity.

## Evidence Flow

```text
Assessment
+
Projects
+
Training
+
Certificates
+
Internships
+
Competitions
+
Achievements
      ↓
Evidence Engine
      ↓
Verified Skills
      ↓
Skill Passport
      ↓
Portfolio
      ↓
Resume
      ↓
Career Profile
```

## Skill Passport

The Student can have:

```text
Verified Skills
Projects
Certifications
Internship Experience
Achievements
Competition Results
Skill Evidence
Career Progress
```

## Evidence-Based Skill Example

```text
Python
 ├── Assessment: 82%
 ├── Project: API Project
 ├── Certificate
 └── Internship evidence when available
```

Result:

```text
Python
Level = Intermediate
Confidence = High
Evidence Count = 3+
```

Only evidence actually available in the Student system should be used.

---

# Resume Generation

```text
Verified Profile
+
Verified Skills
+
Projects
+
Internships
+
Achievements
+
Education
      ↓
Resume Generation
      ↓
Structured Resume
      ↓
LLM Wording / Formatting
```

The LLM must not invent:

- Skills
- Projects
- Certifications
- Experience
- Achievements

It can improve wording based only on supplied verified data.

---

# Portfolio

```text
Verified Evidence
      ↓
Portfolio Builder
      ↓
Projects
Skills
Experience
Achievements
      ↓
Student Portfolio
```

---

# Cross-Cutting Student Services

These are supporting services, not additional top-level Student features.

## Authentication

```text
JWT
+
Argon2 Password Hashing
+
Role-based Authorization
```

## Notifications

Used by:

```text
Achiever AI → GEMS reminders
Internship → Matching opportunity
Application → Status update
Mentorship → Request/session update
Training → New training/workshop
Competition → Deadline
Documents → Verification update
```

## Background Processing

Use background workers for:

```text
Embedding generation
Document processing
OCR
Recommendation refresh
Notifications
GEMS scheduling
Analytics
```

Potential technologies:

- Celery
- Redis
- Celery Beat / APScheduler

---

# Student Module Backend Structure

```text
backend/
│
├── api/
│   └── v1/
│       ├── auth/
│       ├── student/
│       ├── assessments/
│       ├── skills/
│       ├── achiever/
│       ├── internships/
│       ├── mentorship/
│       ├── training/
│       ├── competitions/
│       ├── documents/
│       └── portfolio/
│
├── services/
│   ├── profile_service.py
│   ├── assessment_service.py
│   ├── skill_service.py
│   ├── evidence_service.py
│   ├── skill_gap_service.py
│   ├── roadmap_service.py
│   ├── gems_service.py
│   ├── matching_service.py
│   ├── internship_service.py
│   ├── mentorship_service.py
│   ├── training_service.py
│   ├── competition_service.py
│   ├── document_service.py
│   ├── portfolio_service.py
│   └── notification_service.py
│
├── ai/
│   ├── embeddings.py
│   ├── retrieval.py
│   ├── reranker.py
│   ├── llm.py
│   ├── prompts.py
│   ├── recommendation.py
│   ├── matching.py
│   ├── roadmap.py
│   └── grounding.py
│
├── models/
├── schemas/
├── repositories/
├── workers/
└── core/
```

---

# Student Module Data Foundation

## PostgreSQL

Primary transactional entities:

```text
users
students
student_academic_profiles
career_roles
student_career_goals

skills
skill_categories
role_skills
skill_dependencies
student_skills
skill_evidence

assessments
assessment_questions
assessment_options
assessment_attempts
assessment_answers

roadmaps
roadmap_milestones
roadmap_tasks
student_task_progress

internship_opportunities
opportunity_skills
opportunity_eligibility
internship_applications
application_status_history
internship_enrollments
internship_tasks
internship_evaluations

mentors
mentor_expertise
mentor_availability
mentor_verifications
mentorship_requests
mentorship_connections
mentorship_sessions
mentor_feedback

training
workshops
competitions
achievements

documents
projects
certifications
portfolio
```

---

# Vector Data

Initial vector database:

**PostgreSQL + pgvector**

Potential embeddings:

```text
career_roles
skills
learning_resources
internship_opportunities
mentors
competitions
projects
```

The exact vector entities should be introduced when their corresponding Student feature is implemented.

---

# API Foundation

## Profile

```text
GET    /api/v1/student/profile
PUT    /api/v1/student/profile

GET    /api/v1/student/career-goal
PUT    /api/v1/student/career-goal
```

## Assessment

```text
GET    /api/v1/student/assessments
GET    /api/v1/student/assessments/{id}
POST   /api/v1/student/assessments/{id}/attempt
POST   /api/v1/student/assessments/{id}/submit
```

## Skills

```text
GET    /api/v1/student/skills
GET    /api/v1/student/skills/{skill_id}
GET    /api/v1/student/skill-gaps
```

## Achiever AI

```text
POST   /api/v1/student/achiever/analyze
GET    /api/v1/student/achiever/roadmap
POST   /api/v1/student/achiever/roadmap/regenerate

GET    /api/v1/student/gems/today
POST   /api/v1/student/gems/tasks/{id}/complete
```

## Internships

```text
GET    /api/v1/student/internships/recommended
GET    /api/v1/student/internships/{id}
POST   /api/v1/student/internships/{id}/apply
GET    /api/v1/student/applications
```

## Mentorship

```text
GET    /api/v1/student/mentors
GET    /api/v1/student/mentors/recommended
POST   /api/v1/student/mentorship/requests
GET    /api/v1/student/mentorship/connections
```

## Documents

```text
POST   /api/v1/student/documents
GET    /api/v1/student/documents
GET    /api/v1/student/documents/{id}/download
DELETE /api/v1/student/documents/{id}
```

## Career Profile

```text
GET    /api/v1/student/verified-skills
GET    /api/v1/student/portfolio
GET    /api/v1/student/resume
```

---

# Student Module Security

Required controls:

```text
Authentication
      ↓
Authorization
      ↓
Resource Ownership
      ↓
Input Validation
      ↓
Rate Limiting
      ↓
Audit Logging
```

Use:

- JWT
- Argon2
- HTTPS
- Private object storage
- Signed URLs
- File validation
- Malware scanning
- Database constraints
- Audit logs

---

# Student Module Implementation Dependency Rules

These rules are mandatory during Student implementation.

## Rule 1 — Do not design College relationships yet

College features have not been defined.

Therefore:

```text
Do NOT assume:
Student → College Placement
Student → Faculty Approval
Student → College Internship Approval
Student → College Analytics
```

These will be defined later.

---

## Rule 2 — Do not design Industry relationships yet

Industry features have not been defined.

Therefore:

```text
Do NOT assume:
Student → Company
Student → Industry Recruiter
Student → Company Opportunity Publisher
Student → Industry Evaluation
```

unless the Student-side feature can genuinely operate independently.

---

## Rule 3 — Keep future integration possible

Database and API structures should avoid unnecessary coupling.

Use extensible IDs and relationship structures where future modules may connect, but do not implement unknown workflows.

---

## Rule 4 — Student features must work independently

A Student feature should not be blocked simply because College or Industry modules do not exist.

For example:

```text
Student Profile       → Works now
Assessment            → Works now
Skill Profile         → Works now
Achiever AI           → Works now
GEMS                  → Works now
Mentorship            → Works now
Training              → Works now
Documents             → Works now
Portfolio             → Works now
```

---

## Rule 5 — Future dependencies are explicit

When a future College/Industry dependency is genuinely required, implement the Student-side contract only and mark the external integration as pending.

Example:

```text
Student Internship Module
        ↓
Student Application + Tracking
        ↓
[Future Opportunity Provider Integration]
        ↓
College / Industry module later
```

Do not invent the provider workflow now.

---

# Student Module End-to-End Lifecycle

```text
STUDENT
   ↓
Profile
   ↓
Career Goal
   ↓
Assessment
   ↓
Skill Profile
   ↓
Skill Gap
   ↓
Achiever AI
   ↓
RAG
   ↓
Personalized Roadmap
   ↓
GEMS
   ↓
Learning / Training
   ↓
Mentorship
   ↓
Competitions
   ↓
Projects / Evidence
   ↓
Internship
   ↓
Documents / Verification
   ↓
Verified Skills
   ↓
Skill Passport
   ↓
Portfolio
   ↓
Resume
   ↓
Career Growth
   ↓
Reassessment
   ↓
Updated Skill Profile
   ↓
Updated Skill Gap
   ↓
Updated Roadmap
```

---

# Final Student Module Definition

The Student Module is a **closed-loop skill acceleration system**:

```text
ASSESS
  ↓
UNDERSTAND
  ↓
IDENTIFY GAPS
  ↓
PLAN
  ↓
EXECUTE
  ↓
GAIN EXPERIENCE
  ↓
COLLECT EVIDENCE
  ↓
VERIFY
  ↓
BUILD CAREER PROFILE
  ↓
REASSESS
  ↓
IMPROVE
```

### Three implementation phases

```text
PHASE 1
Foundation & Skill Intelligence
────────────────────────────────
Profile
Career Goal
Assessment
Skill Profile
Skill Gap


PHASE 2
AI Development & Engagement
────────────────────────────────
Achiever AI
RAG
Personalized Roadmap
GEMS
Training
Workshops
Mentorship
Community
Competitions
Achievements


PHASE 3
Career Execution & Verification
────────────────────────────────
Internships
Application Tracking
Documents
Evidence
Verified Skills
Skill Passport
Portfolio
Resume
Career Growth
```

**Scope boundary:** This document defines only the Student Module. College and Industry architectures and their relationships will be designed separately after their feature sets are defined.
