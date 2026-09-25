# SKILLY — Technical Architecture
## Academia–Industry Skill Acceleration & Placement Platform

**Version:** 1.0  
**Architecture Principle:** Evidence-driven, hybrid intelligence, RAG-grounded personalization

---

## 1. Architecture Vision

SKILLY should not implement each feature as an isolated CRUD module.

The platform is built around a **common Intelligence Core** that converts:

`Student Profile → Assessment → Evidence → Skill Profile → Skill Gap → Semantic Retrieval → RAG → AI Personalization → Action → Progress → Reassessment`

The seven Student-facing features consume this common intelligence layer:

1. Student Profile & Career Goal
2. Skill Assessment & Skill Profile
3. Achiever AI
4. Internship Management & Tracking
5. Training, Workshops, Mentorship & Student Engagement
6. Secure Document Management
7. Career Growth & Verified Profile

**GEMS is an internal execution component of Achiever AI, not a separate top-level feature.**

---

# 2. High-Level Architecture

```text
┌──────────────────────────────────────────────────────────────────┐
│                         React Frontend                           │
│                                                                  │
│ Profile | Assessment | Achiever AI | Internships | Mentorship   │
│ Training | Competitions | Documents | Career / Portfolio        │
└──────────────────────────────┬───────────────────────────────────┘
                               │ HTTPS / REST
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                         FastAPI API Layer                        │
│                                                                  │
│ Authentication | Authorization | Validation | Rate Limiting      │
└──────────────────────────────┬───────────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                         Service Layer                            │
│                                                                  │
│ Profile | Assessment | Skill | Achiever | Internship            │
│ Mentorship | Training | Competition | Document | Portfolio       │
└──────────────────────────────┬───────────────────────────────────┘
                               │
              ┌────────────────┴─────────────────┐
              ▼                                  ▼
┌──────────────────────────────┐     ┌────────────────────────────┐
│      Intelligence Core       │     │     Platform Services      │
│                              │     │                            │
│ Skill Gap Engine             │     │ Notification               │
│ Matching Engine              │     │ Background Jobs            │
│ Semantic Search              │     │ Verification               │
│ RAG Retrieval                │     │ File Storage               │
│ Reranking                    │     │ Audit / Logging             │
│ LLM Personalization         │     │ Analytics                  │
└──────────────┬───────────────┘     └──────────────┬─────────────┘
               │                                    │
               └────────────────┬───────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                         Data Layer                               │
│                                                                  │
│ PostgreSQL + pgvector | Redis | Object Storage                   │
└──────────────────────────────────────────────────────────────────┘
```

---

# 3. Core Architecture Principle — Hybrid Intelligence

SKILLY uses three classes of intelligence.

## 3.1 Deterministic Engine

Used where the result must be controlled and auditable.

Examples:

- Assessment scoring
- Eligibility checks
- Skill-gap calculation
- Skill prerequisites
- Application status
- Progress tracking
- Document authorization
- Verification state
- Notification rules

Technology:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy

---

## 3.2 Semantic / ML Engine

Used where similarity or relevance must be calculated.

Examples:

- Skill similarity
- Internship matching
- Mentor matching
- Training recommendation
- Resource retrieval
- Career-role similarity
- Semantic search

Technology:

- Embedding models
- pgvector
- Sentence Transformers / BGE
- Cross-encoder reranking

---

## 3.3 LLM Engine

Used for personalization and language generation.

Examples:

- Personalized roadmap generation
- Roadmap explanations
- Learning-plan generation
- Career guidance
- Resource summarization
- Resume wording
- Natural-language career assistant

The LLM should receive **verified structured evidence and retrieved trusted context**, not blindly infer from a profile.

---

# 4. Common Intelligence Core

```text
                 ┌──────────────────────┐
                 │ Student Profile      │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Assessment Engine    │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Evidence Engine      │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Skill Profile        │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Skill Gap Engine     │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Skill Dependency     │
                 │ Graph                │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Hybrid Retrieval     │
                 │ Metadata + Vector    │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Reranking            │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ RAG Context          │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ LLM Personalization  │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Recommendation /    │
                 │ Roadmap / Guidance   │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Action + Progress    │
                 └──────────┬───────────┘
                            │
                            └──────► Reassessment
```

---

# 5. Student Profile & Career Goal

## Purpose

Create the structured foundation for all downstream intelligence.

## Data

```text
Student
 ├── Personal Information
 ├── Academic Profile
 ├── Career Interests
 ├── Target Career Role
 ├── Target Industry
 └── Career Preferences
```

## Technology

- React forms
- FastAPI
- Pydantic validation
- PostgreSQL
- SQLAlchemy
- JWT authentication

## Core Tables

```text
users
students
student_academic_profiles
career_roles
student_career_goals
career_role_skills
skill_proficiency_levels
```

## Principle

The backend derives the authenticated student from JWT/session context.

Do not trust a client-supplied `student_id` for authorization.

---

# 6. Skill Assessment & Skill Profile

## Assessment Pipeline

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

## Assessment Types

- Technical
- Soft skill
- Aptitude
- Role-specific
- Scenario-based
- Coding / practical assessment where applicable

## Technology

- FastAPI
- PostgreSQL
- Python scoring engine
- Redis for temporary assessment state where needed

## Advanced Assessment

Future adaptive assessment can use:

- Item Response Theory (IRT)
- Computerized Adaptive Testing (CAT)
- Difficulty-based question selection

Example:

```text
Easy → Correct
       ↓
Medium → Correct
       ↓
Hard → Wrong
       ↓
Estimated proficiency updated
```

## Core Tables

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

# 7. Evidence-Based Skill Profile

A skill should not be represented only as:

```text
Python = Advanced
```

Instead:

```text
Skill: Python

Level: Intermediate

Evidence:
 ├── Assessment: 82%
 ├── Projects: 2
 ├── Certification: 1
 ├── Internship: 1
 └── Industry Evaluation: 4/5

Confidence: 0.86
Last Evaluated: <timestamp>
```

## Skill Model

```text
Skill
+ Proficiency
+ Score
+ Confidence
+ Evidence
+ Evidence Source
+ Recency
```

This evidence layer is the foundation for Achiever AI and Career Growth.

---

# 8. Achiever AI Architecture

Achiever AI is the central intelligence feature.

It includes:

- Skill Gap Analysis
- Technical + Soft Skill Analysis
- Industry / Company / Role Requirement Analysis
- Personalized Roadmap
- Relevant Courses / Resources
- GEMS

## Main Pipeline

```text
Student Profile
      ↓
Assessment Results
      ↓
Verified Skill Profile
      ↓
Target Role Requirements
      ↓
Skill Gap Engine
      ↓
Skill Dependency Graph
      ↓
Hybrid Retrieval
      ↓
Reranking
      ↓
RAG Context
      ↓
LLM Personalization
      ↓
Personalized Roadmap
      ↓
GEMS Daily Execution
      ↓
Progress / New Evidence
      ↓
Reassessment
```

---

# 9. Skill Gap Engine

Suppose a Backend Developer role requires:

```text
Python        4/5
SQL           4/5
FastAPI       3/5
Docker        3/5
Git           3/5
System Design 3/5
Communication 4/5
```

Student:

```text
Python        3/5
SQL           2/5
FastAPI       1/5
Docker        0/5
Git           3/5
System Design 1/5
Communication 2/5
```

Basic gap:

```text
Gap = Required Level - Current Level
```

But priority should consider more than gap size.

Conceptual priority:

```text
Priority =
Gap Severity
× Role Importance
× Skill Dependency
× Student Goal Relevance
× Assessment Confidence
```

The exact weights should be configurable rather than hardcoded in the frontend.

---

# 10. Skill Dependency Graph

Skills have prerequisites and dependencies.

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

## Technology

Initial implementation:

- PostgreSQL for persistent skill relationships
- NetworkX for graph computation

Possible later scale option:

- Neo4j

The graph determines learning order and prevents the roadmap from recommending advanced topics before prerequisites.

---

# 11. RAG Architecture

Achiever AI should not generate a roadmap from profile data alone.

## Retrieval Pipeline

```text
Skill Gap
   ↓
Query Construction
   ↓
Metadata Filtering
   ↓
Embedding Generation
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

## Vector Database

Recommended initial choice:

**PostgreSQL + pgvector**

Reason:

- PostgreSQL is already the primary database
- Structured metadata and vector data can be queried together
- Lower infrastructure complexity for MVP

Possible later alternatives:

- Qdrant
- Weaviate
- Pinecone

---

# 12. RAG Knowledge Base

The knowledge base should contain trusted, canonical platform data.

```text
Career Role Requirements
Industry Skill Requirements
Learning Resources
Courses
Documentation
Projects
Practice Problems
Certifications
Interview Topics
Soft Skill Resources
Internship Requirements
Training Programs
```

## Resource Metadata

Example:

```json
{
  "skill": "Docker",
  "level": "Intermediate",
  "role": "Backend Developer",
  "resource_type": "course",
  "difficulty": "medium",
  "duration_hours": 12,
  "source": "verified",
  "language": "English"
}
```

---

# 13. Hybrid Retrieval

Pure vector search is not sufficient.

Use:

```text
Metadata Filtering
        +
Vector Similarity
        +
Reranking
```

Example query:

```text
Skill = Docker
Role = Backend Developer
Level = Intermediate
Duration <= available learning time
Source = verified
```

Then semantic similarity identifies the most relevant resources.

---

# 14. Reranking

Retrieved resources should be ranked using:

```text
Embedding Similarity
+
Skill Relevance
+
Role Relevance
+
Difficulty Match
+
Duration Match
+
Quality
+
Recency
```

Advanced option:

- BGE Cross-Encoder
- Other cross-encoder reranker

MVP option:

- Weighted deterministic ranking

---

# 15. LLM Personalization Layer

The LLM should receive structured context.

Example:

```text
Student:
Python = 3/5
SQL = 2/5
Docker = 0/5

Target:
Backend Developer

Priority Gaps:
Docker
SQL
FastAPI

Skill Dependencies:
Python → FastAPI → API → Docker

Available Time:
2 hours/day

Retrieved Resources:
Resource A
Resource B
Resource C
```

Instruction:

```text
Generate a personalized learning roadmap using only
the supplied evidence and retrieved resources.

Respect:
- current proficiency
- prerequisites
- available time
- target role
- resource difficulty
```

The LLM output should be structured JSON.

---

# 16. Roadmap Output

Example:

```json
{
  "roadmap": [
    {
      "week": 1,
      "skill": "SQL",
      "objective": "Intermediate SQL",
      "resources": ["resource_123"],
      "practice": ["problem_21"],
      "project": null
    },
    {
      "week": 2,
      "skill": "FastAPI",
      "objective": "Build REST APIs",
      "resources": ["resource_456"],
      "practice": [],
      "project": "Build Task API"
    }
  ]
}
```

The roadmap is then persisted and consumed by GEMS.

---

# 17. GEMS Architecture

GEMS is an execution engine inside Achiever AI.

```text
Personalized Roadmap
       ↓
Goals
       ↓
Milestones
       ↓
Tasks
       ↓
Dependencies
       ↓
Daily Scheduling
       ↓
Reminder
       ↓
Student Completion
       ↓
Progress Update
```

## Technologies

- PostgreSQL
- Redis
- Celery / Celery Beat
- APScheduler where appropriate
- Firebase Cloud Messaging for push notifications

## Example

```text
Week 1
 ├── Learn SQL Joins
 ├── Solve 10 SQL Problems
 ├── Complete Mini Assessment
 └── Build Database Query Task
```

GEMS schedules these according to:

- roadmap dependencies
- available time
- task duration
- student progress
- deadlines

---

# 18. Internship Management & Tracking

Internship recommendation uses the same Intelligence Core.

```text
Student Skills
      +
Career Goal
      +
Skill Gaps
      +
Eligibility
      +
Internship Requirements
      ↓
Hard Eligibility Filter
      ↓
Skill Matching
      ↓
Semantic Matching
      ↓
Ranking
      ↓
Relevant Internships
```

## Matching Inputs

```text
Student:
 ├── Skills
 ├── Skill Levels
 ├── Career Goal
 ├── Projects
 ├── Education
 └── Preferences

Internship:
 ├── Required Skills
 ├── Eligibility
 ├── Role
 ├── Industry
 ├── Description
 └── Location / Mode
```

---

# 19. Internship Matching

Example:

```text
Internship Requirements:
Python
SQL
FastAPI
Git
```

Student:

```text
Python = 4
SQL = 3
FastAPI = 2
Git = 4
```

System can produce:

```text
Skill Match: 82%
Eligibility: PASS
Career Match: HIGH
Primary Gap: FastAPI
```

## Important

Mandatory eligibility requirements are deterministic filters.

AI should not recommend a student who fails a mandatory eligibility condition.

---

# 20. Internship Semantic Matching

Use embeddings for:

```text
Internship Description
Student Career Goal
Student Skills
Projects
Resume / Verified Profile
```

Technology:

```text
Embedding Model
      ↓
pgvector
      ↓
Cosine Similarity
```

Final recommendation can combine:

```text
Eligibility
+
Skill Match
+
Semantic Similarity
+
Career Alignment
+
Experience Match
```

---

# 21. Internship Lifecycle

Application tracking should be deterministic.

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

Maintain:

```text
internship_applications
application_status_history
internship_enrollments
internship_tasks
internship_evaluations
```

Every status transition should be auditable.

---

# 22. Training Recommendation

Training recommendations use:

```text
Skill Gap
      ↓
Required Skill
      ↓
Metadata Filter
      ↓
Vector Search
      ↓
Reranking
      ↓
Recommended Training
```

Example:

```text
Gap = Docker Intermediate

Retrieve:
 ├── Docker Course
 ├── Docker Workshop
 ├── Docker Lab
 └── Docker Certification
```

---

# 23. Workshop Recommendation

Workshops can be matched using:

```text
Career Goal
+
Skill Gap
+
Interests
+
Role
+
Eligibility
```

The same semantic retrieval infrastructure can be reused.

---

# 24. Mentorship Architecture

Mentorship is an **open mentorship platform**.

Potential mentors may include:

- Faculty
- Successful seniors
- Alumni
- Developers
- Industry professionals
- Researchers
- Entrepreneurs
- Domain experts
- Other qualified mentors

## Mentor Pipeline

```text
Mentor Registration
      ↓
Mentor Profile
      ↓
Expertise
      ↓
Experience
      ↓
Availability
      ↓
Verification
      ↓
Mentor Search Index
```

Registration and verification are separate states.

```text
Registered ≠ Verified
```

---

# 25. Mentor Matching

Student:

```text
Target = Backend Developer
Gap = System Design
Interest = Distributed Systems
```

Mentor:

```text
Expertise = Backend
Experience = 8 years
Topics = System Design, APIs
```

Matching can combine:

```text
Career Similarity
+
Skill Similarity
+
Topic Similarity
+
Experience
+
Availability
+
Student Level
```

Semantic pipeline:

```text
Student Mentorship Intent
       ↓
Embedding
       ↓
Mentor Embeddings
       ↓
pgvector
       ↓
Top Relevant Mentors
       ↓
Structured Filters
```

---

# 26. Mentorship Lifecycle

```text
Student
   ↓
Search / Recommended Mentors
   ↓
View Mentor
   ↓
Request Mentorship
   ↓
Accept / Decline
   ↓
Mentorship Connection
   ↓
Sessions
   ↓
Action Items
   ↓
Feedback
```

Core tables:

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

---

# 27. Competitions / Hackathons

Recommendation:

```text
Student Skills
+
Career Interests
+
Target Role
+
Competition Requirements
+
Eligibility
      ↓
Matching
      ↓
Semantic Search
      ↓
Ranking
      ↓
Relevant Competitions
```

Lifecycle:

```text
View
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

# 28. Secure Document Management

Document management should use security-first architecture.

```text
React
  ↓
FastAPI
  ↓
Authorization
  ↓
File Validation
  ↓
Object Storage
  ↓
Metadata in PostgreSQL
```

## Storage

Recommended options:

- AWS S3
- Cloudflare R2
- Supabase Storage
- Azure Blob

## Database

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

Actual files should not be stored inside PostgreSQL.

---

# 29. Secure Download

```text
Student Request
      ↓
JWT Authentication
      ↓
Ownership / Permission Check
      ↓
Generate Signed URL
      ↓
Temporary File Access
```

Documents should be private by default.

---

# 30. Document Intelligence

AI can assist with document processing.

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
Validation
 ↓
Admin / Trusted Verification
 ↓
Evidence
```

Technologies:

- ClamAV
- Tesseract / cloud OCR
- Document parser
- LLM structured extraction

Possible extracted information:

```text
Organization
Role
Duration
Skills
Project
Certificate ID
Date
```

Extracted data should not automatically become verified evidence.

---

# 31. Career Growth & Verified Profile

This is the final evidence/output layer.

## Evidence Graph

```text
Student
  │
  ├── Assessment
  ├── Project
  ├── Internship
  ├── Certification
  ├── Competition
  ├── Workshop
  └── Industry Evaluation
          ↓
     Skill Evidence
          ↓
     Skill Confidence
          ↓
     Verified Skill
```

Example:

```text
Python
 ├── Assessment: 82%
 ├── Project: API Project
 ├── Internship: Backend Intern
 └── Certificate
```

Result:

```text
Python
Level = Intermediate
Confidence = High
Evidence Count = 4
```

---

# 32. Skill Passport

The verified profile should expose:

```text
Verified Skills
Projects
Certifications
Internships
Achievements
Competition Results
Industry Evaluations
Skill Evidence
Career Progress
```

The key principle is:

**Proof-backed skills instead of self-declared skills.**

---

# 33. Resume Generation

Resume generation should use verified platform data.

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

- achievements
- experience
- projects
- certifications
- skills

It may improve wording using supplied verified data.

---

# 34. Portfolio Generation

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
Public / Private Portfolio
```

AI can help summarize project descriptions while remaining grounded in stored evidence.

---

# 35. AI Platform Layer

Do not create independent AI implementations for every feature.

Build reusable services:

```text
ai/
 ├── embeddings.py
 ├── retrieval.py
 ├── reranker.py
 ├── llm.py
 ├── prompts.py
 ├── recommendation.py
 ├── matching.py
 ├── roadmap.py
 └── grounding.py
```

These services can be reused by:

```text
Achiever AI
Internship Matching
Mentor Matching
Training Recommendation
Competition Recommendation
Career Guidance
Portfolio / Resume
```

---

# 36. Backend Service Architecture

Recommended backend structure:

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
│   ├── notification_worker.py
│   ├── recommendation_worker.py
│   └── embedding_worker.py
│
└── core/
    ├── config.py
    ├── security.py
    ├── database.py
    └── logging.py
```

---

# 37. Data Architecture

## PostgreSQL

Primary transactional data:

```text
users
students
academic_profiles
career_roles
career_goals

skills
skill_categories
role_skills
skill_dependencies
student_skills
skill_evidence

assessments
assessment_questions
assessment_attempts
assessment_answers

roadmaps
roadmap_milestones
roadmap_tasks
student_task_progress

companies
opportunities
opportunity_skills
opportunity_eligibility
internship_applications
application_status_history
internship_enrollments
internship_evaluations

mentors
mentor_expertise
mentor_availability
mentor_verifications
mentorship_requests
mentorship_connections
mentorship_sessions

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

# 38. Vector Data Architecture

Use pgvector for embeddings.

Potential vector entities:

```text
resource_embeddings
career_role_embeddings
internship_embeddings
mentor_embeddings
skill_embeddings
competition_embeddings
document_embeddings
project_embeddings
```

Example:

```text
mentor_id
embedding
expertise_metadata
availability_metadata
verification_status
```

---

# 39. Redis

Use Redis for:

- caching
- temporary assessment state
- rate limiting
- task queues
- frequently accessed recommendations
- session-related short-lived data

Do not use Redis as the source of truth for important student records.

---

# 40. Background Processing

Some operations should not block API requests.

Use Celery / workers for:

```text
Embedding generation
Document processing
OCR
Recommendation refresh
Notification scheduling
Daily GEMS generation
Email / push notification
Analytics aggregation
```

Example:

```text
Student uploads certificate
        ↓
API stores file
        ↓
Queue background job
        ↓
OCR / extraction
        ↓
Verification workflow
        ↓
Evidence update
```

---

# 41. Notification Architecture

Notifications are a cross-cutting service, not an additional top-level Student feature.

Sources:

```text
Achiever AI → GEMS reminder
Internship → New matching internship
Application → Status update
Mentorship → Request / session update
Training → New training
Competition → Deadline
Documents → Verification update
```

Pipeline:

```text
Event
 ↓
Notification Service
 ↓
Preference Check
 ↓
Channel Selection
 ↓
In-App / Email / Push
```

---

# 42. Explainability

Recommendations should provide reasons.

Example:

```text
Recommended Internship

Why?
✓ Matches your Backend Developer goal
✓ 3/4 required skills already demonstrated
✓ FastAPI is your main remaining gap
✓ Eligibility requirements satisfied
```

For a mentor:

```text
Why this mentor?

✓ Backend expertise
✓ System Design experience
✓ Matches your target role
✓ Available during your preferred time
```

This makes AI recommendations more transparent.

---

# 43. AI Grounding Rules

The AI system should follow these rules:

1. Use verified student evidence.
2. Use canonical role requirements.
3. Retrieve trusted resources before generation.
4. Respect hard eligibility constraints.
5. Do not fabricate achievements or certifications.
6. Do not invent internship requirements.
7. Return structured outputs where possible.
8. Store recommendation reasons.
9. Keep deterministic business rules outside the LLM.
10. Recalculate recommendations when important student evidence changes.

---

# 44. Continuous Learning Loop

The platform should continuously update the student's state.

```text
Assessment
   ↓
Skill Profile
   ↓
Skill Gap
   ↓
Roadmap
   ↓
GEMS
   ↓
Learning
   ↓
Practice
   ↓
Project
   ↓
Internship / Mentorship
   ↓
New Evidence
   ↓
Updated Skill Profile
   ↓
Reassessment
   ↓
Updated Skill Gap
   ↓
Updated Roadmap
```

This is what turns SKILLY from a static portal into a **continuous skill acceleration platform**.

---

# 45. API Architecture

Example APIs:

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

## Internship

```text
GET    /api/v1/student/internships/recommended
GET    /api/v1/student/internships/{id}
POST   /api/v1/student/internships/{id}/apply
GET    /api/v1/student/applications
```

## Mentorship

```text
GET    /api/v1/mentors
GET    /api/v1/mentors/recommended
POST   /api/v1/mentorship/requests
GET    /api/v1/mentorship/connections
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

# 46. Security Architecture

Core controls:

```text
JWT Authentication
       ↓
Role-Based Authorization
       ↓
Resource Ownership Checks
       ↓
Input Validation
       ↓
Rate Limiting
       ↓
Audit Logging
```

Additional controls:

- Argon2 password hashing
- HTTPS
- Private object storage
- Signed temporary URLs
- File type and size validation
- Malware scanning
- Secrets in environment/secret manager
- Database constraints
- Audit trail for verification and application status

---

# 47. Observability

Monitor:

```text
API latency
Error rate
Database performance
Queue latency
AI request latency
Embedding failures
RAG retrieval quality
Recommendation acceptance
Roadmap completion
Notification delivery
```

Technology options:

- Structured application logs
- Prometheus
- Grafana
- OpenTelemetry

---

# 48. Recommendation Quality Metrics

The AI system should be measurable.

## Achiever AI

```text
Roadmap completion rate
Task completion rate
Skill improvement
Reassessment improvement
Resource relevance feedback
```

## Internship

```text
Recommendation click rate
Application rate
Shortlist rate
Skill-match accuracy
```

## Mentorship

```text
Recommendation acceptance
Mentorship request acceptance
Session completion
Student feedback
```

## Training

```text
Enrollment
Completion
Skill improvement
```

---

# 49. Final Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | FastAPI |
| API Validation | Pydantic |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Vector Search | pgvector |
| Embeddings | Sentence Transformers / BGE |
| Reranking | Cross-Encoder / BGE Reranker |
| LLM | GPT-class / compatible LLM API |
| RAG | Custom Retrieval + LangChain/LlamaIndex where useful |
| Cache | Redis |
| Background Jobs | Celery |
| Scheduler | Celery Beat / APScheduler |
| File Storage | S3 / Cloudflare R2 / Supabase Storage |
| OCR | Tesseract / Cloud OCR |
| Malware Scan | ClamAV |
| Authentication | JWT + Argon2 |
| Push Notifications | Firebase Cloud Messaging |
| Skill Graph | NetworkX initially |
| Monitoring | Prometheus + Grafana |
| Deployment | Docker |

---

# 50. Final System Architecture

```text
                         SKILLY
                           │
                           ▼
                 ┌─────────────────────┐
                 │    Student Layer    │
                 │ Profile + Goals     │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Assessment Engine   │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Evidence Engine    │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Skill Intelligence  │
                 │ Profile + Graph     │
                 └──────────┬──────────┘
                            ▼
        ┌───────────────────┴────────────────────┐
        │            INTELLIGENCE CORE           │
        │                                        │
        │ Skill Gap │ Matching │ Embeddings      │
        │ Vector DB │ RAG      │ Reranking       │
        │ LLM       │ Grounding│ Recommendation  │
        └───────────────────┬────────────────────┘
                            ▼
        ┌───────────────────┼────────────────────┐
        │                   │                    │
        ▼                   ▼                    ▼
   Achiever AI         Internship           Mentorship
        │               Matching              Matching
        ▼                   │                    │
      GEMS                 ▼                    ▼
        │              Applications          Sessions
        │
        └──────────────────┬─────────────────────
                           ▼
                Training / Competitions
                           │
                           ▼
                  New Verified Evidence
                           │
                           ▼
                  Career Growth Profile
                           │
                           ▼
                     Reassessment
                           │
                           └──────────────► LOOP
```

## Architectural Definition

**SKILLY = Transactional Platform + Evidence Engine + Semantic Intelligence + RAG + LLM Personalization + Continuous Feedback Loop.**

The most important implementation rule is:

> **Deterministic systems decide facts and constraints. Semantic systems find relevance. RAG supplies trusted context. LLMs personalize and explain. Evidence and feedback continuously update the student's skill state.**
