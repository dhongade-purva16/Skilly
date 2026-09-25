# SKILLY --- Student Module

## Product Requirements Document (PRD)

**Product:** SKILLY\
**Module:** Student\
**Version:** 1.1\
**Status:** Product Definition

------------------------------------------------------------------------

# 1. Product Vision

SKILLY provides a connected student career-development lifecycle instead
of a collection of disconnected features.

The platform helps students:

-   Build their academic and career profile
-   Assess technical, soft-skill and aptitude capabilities
-   Identify skill gaps against career/industry requirements
-   Receive an AI-powered personalized roadmap
-   Execute roadmap tasks day-by-day through GEMS
-   Discover and manage relevant internships
-   Access training, workshops and mentorship
-   Participate in competitions and community activities
-   Maintain secure career and academic documents
-   Build a verified professional profile

## Core Journey

``` text
Student Profile
      ↓
Career Goal
      ↓
Skill Assessment
      ↓
Skill Profile
      ↓
Achiever AI
      ↓
Skill Gap Analysis
      ↓
Personalized Roadmap
      ↓
GEMS — Daily Execution
      ↓
Learning / Practice / Experience
      ↓
Internships / Mentorship / Competitions
      ↓
Verified Evidence
      ↓
Career Growth & Readiness
      ↓
Continuous Reassessment
```

------------------------------------------------------------------------

# 2. Target User

## Primary User --- Student

A college/university student who wants to:

-   Understand current skills
-   Identify suitable career paths
-   Improve industry-relevant skills
-   Follow a personalized learning plan
-   Find internships
-   Get guidance from mentors
-   Participate in practical activities
-   Build a verified career profile

------------------------------------------------------------------------

# 3. Student Module --- 7 Major Features

1.  **Student Profile & Career Goal**
2.  **Skill Assessment & Skill Profile**
3.  **Achiever AI --- Skill Gap, Roadmap & GEMS**
4.  **Internship Management & Tracking**
5.  **Training, Workshops, Mentorship & Student Engagement**
6.  **Secure Document Management**
7.  **Career Growth & Verified Profile**

The features are intentionally integrated so related functionality is
handled inside one major feature rather than creating unnecessary
standalone modules.

------------------------------------------------------------------------

# 4. Feature 1 --- Student Profile & Career Goal

## Objective

Create a complete student identity containing personal, academic and
career information.

## Personal Profile

-   Full name
-   Email
-   Mobile number
-   Profile photo
-   Location
-   Bio
-   LinkedIn
-   GitHub
-   Personal website

## Academic Profile

-   College / Institution
-   Department
-   Degree
-   Branch
-   Roll number
-   Semester / Year
-   Graduation year
-   Academic performance
-   Academic records

## Career Profile

-   Career interests
-   Target career role
-   Preferred industry
-   Preferred domain
-   Preferred work location/mode

## Flow

``` text
Registration
    ↓
Personal Profile
    ↓
Academic Profile
    ↓
Career Interests
    ↓
Target Career Selection
    ↓
Student Career Profile
```

The profile becomes an input to assessment, matching and Achiever AI.

------------------------------------------------------------------------

# 5. Feature 2 --- Skill Assessment & Skill Profile

## Objective

Measure the student's current capability and create a structured skill
profile.

## Assessment Types

-   Technical assessment
-   Soft-skill assessment
-   Aptitude assessment
-   Career/role-specific assessment
-   Industry/company-oriented assessment where valid assessment data is
    available

## Assessment Flow

``` text
Target Career
      ↓
Required Skills
      ↓
Assessment Selection
      ↓
Questions
      ↓
Student Attempts
      ↓
Submit
      ↓
Evaluation
      ↓
Skill-wise Scores
      ↓
Current Skill Profile
```

## Skill Profile

Each skill may contain:

-   Skill name
-   Category
-   Proficiency level
-   Assessment score
-   Evidence
-   Verification status
-   Assessment date

Example:

``` text
Python         → Advanced
SQL            → Intermediate
FastAPI        → Beginner
Docker         → Beginner
Communication  → Advanced
```

The Skill Profile becomes a major input to Achiever AI and internship
matching.

------------------------------------------------------------------------

# 6. Feature 3 --- Achiever AI

## Objective

Achiever AI is the intelligent career-development engine of the Student
Module.

It uses:

``` text
Student Profile
       +
Academic Profile
       +
Target Career
       +
Skill Profile
       +
Assessment Results
       +
Industry / Role Requirements
       ↓
ACHIEVER AI
```

## 6.1 Skill Gap Analysis

``` text
Required Skill Level
        -
Current Skill Level
        =
Skill Gap
```

The system identifies:

-   Missing skills
-   Weak skills
-   Critical skills
-   Technical gaps
-   Soft-skill gaps
-   Priority gaps

------------------------------------------------------------------------

## 6.2 Industry / Role Requirement Analysis

``` text
Student Skills
      +
Target Role
      +
Industry Requirements
      ↓
Requirement Comparison
      ↓
Skill Gap
```

The system should use available canonical industry/role data rather than
inventing requirements.

------------------------------------------------------------------------

## 6.3 Personalized Roadmap

Achiever AI converts identified gaps into a personalized roadmap.

The roadmap can contain:

-   Skill to learn
-   Priority
-   Learning resource
-   Practice activity
-   Project
-   Expected outcome
-   Target completion period

``` text
Skill Gap
   ↓
Priority
   ↓
Skill Dependencies
   ↓
Learning Resources
   ↓
Practice / Projects
   ↓
Personalized Roadmap
```

------------------------------------------------------------------------

## 6.4 GEMS --- Daily Roadmap Execution

**GEMS is part of Achiever AI, not a separate top-level feature.**

GEMS converts the personalized roadmap into daily actionable tasks.

``` text
Personalized Roadmap
       ↓
Break into Goals
       ↓
Break Goals into Tasks
       ↓
Assign Tasks to Days
       ↓
Daily Learning Plan
       ↓
Daily Reminder
       ↓
Student Completes Task
       ↓
Progress Updated
       ↓
Next Tasks
```

Example:

``` text
ROADMAP
Goal: Backend Development

Week 1 → SQL Fundamentals
Week 2 → FastAPI
Week 3 → Authentication
Week 4 → Docker
```

GEMS converts this into:

``` text
MONDAY
[ ] SQL Lesson 1
[ ] Solve 20 SQL Questions

TUESDAY
[ ] SQL Lesson 2
[ ] Practice Queries

WEDNESDAY
[ ] SQL Joins
[ ] Practice

THURSDAY
[ ] Mini SQL Project

FRIDAY
[ ] Assessment
```

### Daily Reminder

``` text
Today's GEMS Tasks

[ ] Complete SQL Lesson
[ ] Solve 20 Questions
[ ] Complete Practice Task

Reminder:
"Your learning task is pending."
```

------------------------------------------------------------------------

## 6.5 Relevant Courses & Resources

Achiever AI recommends resources based on identified gaps and roadmap
requirements.

Possible resources:

-   Courses
-   Tutorials
-   Practice material
-   Projects
-   Certifications
-   Workshops

``` text
Skill Gap
   ↓
Required Skill
   ↓
Resource Retrieval
   ↓
Relevant Resources
   ↓
Roadmap
```

------------------------------------------------------------------------

## 6.6 Continuous Adaptation

The roadmap should be updateable based on student progress.

``` text
Assessment
   ↓
Roadmap
   ↓
GEMS
   ↓
Learning
   ↓
Progress
   ↓
Re-assessment
   ↓
Updated Skill Profile
   ↓
Updated Skill Gap
   ↓
Updated Roadmap
```

------------------------------------------------------------------------

# 7. Feature 4 --- Internship Management & Tracking

## Objective

Provide students with relevant internships based on career interests,
skills and eligibility and manage the complete internship lifecycle.

## Matching Inputs

``` text
Career Interest
      +
Skill Profile
      +
Target Career
      +
Eligibility
      +
Industry Requirements
      +
Student Progress
```

## Internship Discovery

``` text
Student Profile
      ↓
Career Interest
      +
Skills
      ↓
Internship Matching
      ↓
Relevant Internships
      ↓
Student Notifications
```

## Student Actions

-   Search internships
-   Filter internships
-   View company
-   View role
-   View required skills
-   View eligibility
-   View duration
-   View location/work mode
-   Check readiness
-   Apply

## Application Flow

``` text
Internship
    ↓
Eligibility Check
    ↓
Skill / Career Match
    ↓
Apply
    ↓
Application Submitted
    ↓
Application Tracking
```

## Application Status

``` text
Applied
   ↓
Shortlisted
   ↓
Assessment / Interview
   ↓
Selected
   ↓
Internship
```

Possible terminal state:

``` text
Rejected
```

## Internship Progress

``` text
Internship Starts
      ↓
Tasks / Milestones
      ↓
Progress Tracking
      ↓
Mentor / Industry Feedback
      ↓
Final Evaluation
      ↓
Internship Completion
      ↓
Verified Experience
```

Internship outcomes can contribute to the student's Skill Profile,
Evidence, Portfolio and Career Profile.

------------------------------------------------------------------------

# 8. Feature 5 --- Training, Workshops, Mentorship & Student Engagement

## Objective

Provide students with learning opportunities, professional guidance,
practical exposure and participation opportunities.

This integrated feature includes:

-   Training
-   Workshops
-   Mentorship
-   Community
-   Contributions
-   Competitions
-   Achievements

------------------------------------------------------------------------

## 8.1 Training

Includes:

-   Industry training
-   Skill-development programs
-   Certification programs
-   Practical training

### Flow

``` text
Career Goal / Skill Gap
        ↓
Recommended Training
        ↓
Student Enrolls
        ↓
Training
        ↓
Completion
        ↓
Certificate / Evidence
        ↓
Career Profile
```

------------------------------------------------------------------------

# 8.2 Workshops

Students can discover and participate in:

-   Technical workshops
-   Industry workshops
-   Career workshops
-   Expert sessions
-   Practical sessions

``` text
Workshop
   ↓
View Details
   ↓
Register
   ↓
Attend
   ↓
Completion / Participation
   ↓
Evidence
```

------------------------------------------------------------------------

# 8.3 Open Mentorship Platform

## Objective

Mentorship is an open platform where eligible individuals can register
to provide mentorship to students.

Potential mentor categories include:

-   Faculty
-   Experienced students
-   Successful seniors
-   Alumni
-   Industry professionals
-   Developers
-   Researchers
-   Entrepreneurs
-   Domain experts
-   Other qualified professionals

The platform should not assume that only faculty or alumni can become
mentors.

## Mentor Registration

``` text
Potential Mentor
      ↓
Register as Mentor
      ↓
Mentor Profile
      ↓
Select Expertise
      ↓
Select Career Domains
      ↓
Add Experience
      ↓
Set Availability
      ↓
Verification / Approval where required
      ↓
Mentor Listed
```

## Mentor Profile

A mentor may provide:

-   Name
-   Professional title
-   Organization
-   Experience
-   Education
-   Expertise
-   Skills
-   Career domains
-   Mentorship topics
-   Availability
-   Preferred student level
-   Languages
-   Profile links
-   Verification status

## Student Mentor Discovery

``` text
Student
   ↓
Career Goal
   +
Skill Gap
   +
Interest
   ↓
Mentor Search / Matching
   ↓
Relevant Mentors
   ↓
View Mentor Profile
   ↓
Request Mentorship
```

## Mentorship Request

``` text
Student
   ↓
Select Mentor
   ↓
Send Request
   ↓
Mentor Accepts / Declines
   ↓
Mentorship Connection
```

## Mentorship Session

``` text
Mentor + Student
       ↓
Session
       ↓
Discussion / Guidance
       ↓
Action Items
       ↓
Student Progress
       ↓
Mentor Feedback
```

## Personal Mentorship

Students can request one-to-one mentorship based on:

-   Career goal
-   Skill gap
-   Interview preparation
-   Project guidance
-   Academic guidance
-   Industry preparation
-   Career transition
-   Other supported mentorship topics

## Mentor Verification

Depending on mentor category and platform policy, verification may
include:

-   Institution verification
-   Alumni verification
-   Professional profile verification
-   Organization verification
-   Identity verification
-   Admin approval

Verification status should be clearly displayed rather than implying
that every registered mentor is automatically verified.

------------------------------------------------------------------------

# 8.4 Community & Contributions

Students can participate in:

-   Discussions
-   Knowledge sharing
-   Resource sharing
-   Peer support
-   Questions and answers
-   Technical contributions

### Flow

``` text
Student
   ↓
Community Contribution
   ↓
Knowledge / Resource / Discussion / Peer Support
   ↓
Contribution Recorded
   ↓
Recognition / Achievement
```

------------------------------------------------------------------------

# 8.5 Competitions & Hackathons

Students can discover and participate in:

-   Hackathons
-   Coding competitions
-   Innovation challenges
-   Technical competitions
-   Other relevant activities

### Flow

``` text
Competition / Hackathon
        ↓
View Details
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

------------------------------------------------------------------------

# 8.6 Achievement Dashboard

The student's participation and outcomes can be collected into an
achievement dashboard.

Possible records:

-   Competition participation
-   Hackathon participation
-   Awards
-   Certifications
-   Workshop participation
-   Training completion
-   Community contributions
-   Internship achievements
-   Project achievements

------------------------------------------------------------------------

# 9. Feature 6 --- Secure Document Management

## Objective

Provide a secure centralized document vault.

## Document Categories

### Career

-   Resume
-   Portfolio documents
-   Internship records
-   Internship certificates
-   Project documents

### Academic

-   Academic records
-   Marksheets
-   Enrollment documents

### Certifications

-   Course certificates
-   Industry certifications
-   Training certificates

### Achievements

-   Competition certificates
-   Hackathon certificates
-   Awards
-   Recognition documents

## Upload Flow

``` text
Student
   ↓
Upload Document
   ↓
Select Document Type
   ↓
File Validation
   ↓
Secure Storage
   ↓
Metadata
   ↓
Document Vault
```

## Access

``` text
Student
   ↓
Document Vault
   ↓
Authentication
   ↓
Authorization
   ↓
Access Document
```

Documents should not be publicly accessible by default.

------------------------------------------------------------------------

# 10. Feature 7 --- Career Growth & Verified Profile

## Objective

Convert the student's development history into a professional,
evidence-backed career profile.

## Includes

-   Verified Skill Passport
-   Digital Portfolio
-   Resume
-   Projects
-   Certifications
-   Internship experience
-   Achievements
-   Competition results
-   Industry evaluation
-   Skill evidence
-   Career progress

## Evidence Sources

``` text
Assessment
     +
Courses
     +
Projects
     +
Certifications
     +
Internships
     +
Industry Evaluation
     +
Competitions
     +
Mentorship / Activities
     ↓
Verified Evidence
```

## Career Profile Flow

``` text
Student Activities
        ↓
Evidence Collection
        ↓
Verification
        ↓
Verified Skills
        ↓
Skill Passport
        ↓
Digital Portfolio
        ↓
Resume
        ↓
Career Profile
        ↓
Jobs / Placements
```

------------------------------------------------------------------------

# 11. Student Dashboard

The Student Dashboard summarizes the complete journey.

## Career

-   Target Career
-   Career progress
-   Current skill level

## Achiever AI

-   Current roadmap
-   Today's GEMS tasks
-   Pending tasks
-   Daily reminders
-   Roadmap progress

## Skills

-   Strong skills
-   Skill gaps
-   Recently improved skills

## Internship

-   Recommended internships
-   Active applications
-   Application statuses
-   Active internship

## Development

-   Courses
-   Training
-   Workshops
-   Mentorship

## Engagement

-   Competitions
-   Achievements
-   Contributions

## Profile

-   Portfolio
-   Resume
-   Verified skills
-   Documents

------------------------------------------------------------------------

# 12. Notifications

Notifications are a cross-cutting service.

## Sources

``` text
Achiever AI
    ↓
GEMS Daily Reminder

Internship System
    ↓
New Matching Internship

Application System
    ↓
Application Status

Mentorship
    ↓
Mentor Request / Acceptance / Session Update

Training
    ↓
New Training / Workshop

Competition
    ↓
New Competition / Deadline

Documents
    ↓
Verification / Status
```

------------------------------------------------------------------------

# 13. AI Principles

AI supports personalization while deterministic platform logic handles
authoritative decisions.

## Deterministic Logic

Use deterministic logic for:

-   Assessment scoring
-   Eligibility
-   Skill-gap calculation where rules are defined
-   Application status
-   Progress calculation
-   Document access
-   Authorization
-   Verification status

## AI Use Cases

Use AI for:

-   Personalized roadmap generation
-   Resource recommendation
-   Career guidance
-   Semantic skill matching
-   Internship recommendation
-   Mentor discovery/matching
-   Natural-language interaction

AI recommendations should be based on available student data and trusted
platform data. The system should avoid fabricating requirements,
opportunities, certifications or achievements.

------------------------------------------------------------------------

# 14. Cross-Feature Feedback Loop

The Student Module should work as a connected lifecycle.

``` text
PROFILE
   ↓
ASSESSMENT
   ↓
SKILL PROFILE
   ↓
ACHIEVER AI
   ↓
ROADMAP
   ↓
GEMS
   ↓
LEARNING
   ↓
INTERNSHIP
   ↓
MENTORSHIP
   ↓
PROJECTS / COMPETITIONS
   ↓
INDUSTRY / MENTOR EVALUATION
   ↓
VERIFIED EVIDENCE
   ↓
UPDATED SKILL PROFILE
   ↓
ACHIEVER AI
```

Additional feedback paths:

``` text
Training
   ↓
Skills / Evidence
   ↓
Profile

Mentorship
   ↓
Feedback / Guidance
   ↓
Career Development

Competitions
   ↓
Achievements
   ↓
Portfolio

Internship
   ↓
Industry Evaluation
   ↓
Verified Skills
```

------------------------------------------------------------------------

# 15. Complete Student Lifecycle

``` text
                         STUDENT
                            |
                            v
              ┌─────────────────────────┐
              │ 1. PROFILE & CAREER     │
              │    GOAL                 │
              └────────────┬────────────┘
                           ↓
              ┌─────────────────────────┐
              │ 2. ASSESSMENT &         │
              │    SKILL PROFILE        │
              └────────────┬────────────┘
                           ↓
              ┌─────────────────────────┐
              │ 3. ACHIEVER AI          │
              │                         │
              │ Skill Gap               │
              │ Personalized Roadmap    │
              │ Courses                 │
              │ GEMS                    │
              │ Daily Tasks             │
              │ Reminders               │
              └────────────┬────────────┘
                           ↓
              ┌─────────────────────────┐
              │ 4. INTERNSHIP           │
              │ MANAGEMENT & TRACKING   │
              └────────────┬────────────┘
                           ↓
              ┌─────────────────────────┐
              │ 5. TRAINING +           │
              │ WORKSHOPS +             │
              │ MENTORSHIP +            │
              │ COMMUNITY +              │
              │ COMPETITIONS            │
              └────────────┬────────────┘
                           ↓
              ┌─────────────────────────┐
              │ 6. SECURE DOCUMENT      │
              │    MANAGEMENT           │
              └────────────┬────────────┘
                           ↓
              ┌─────────────────────────┐
              │ 7. CAREER GROWTH &      │
              │    VERIFIED PROFILE     │
              └────────────┬────────────┘
                           ↓
                    CAREER READINESS
```

------------------------------------------------------------------------

# 16. Security & Privacy Requirements

-   JWT authentication
-   Role-based authorization
-   Student ownership validation
-   Secure document storage
-   Private-by-default documents
-   Mentor/student access controls
-   Audit logging for important actions
-   Secure password handling
-   API authorization
-   No unauthorized access to student data

Mentor profiles should expose only information intended for discovery.
Private student information must not be exposed to mentors or other
users without appropriate authorization.

------------------------------------------------------------------------

# 17. Scalability Requirements

The architecture should support growth in:

-   Students
-   Colleges
-   Companies
-   Mentors
-   Skills
-   Opportunities
-   Assessments
-   Courses
-   Workshops
-   Competitions
-   Community activity
-   Documents

The mentorship system should support many mentor categories without
requiring separate systems for faculty, alumni, developers or industry
professionals.

------------------------------------------------------------------------

# 18. Auditability

Important actions should be traceable:

-   Assessment submission
-   Skill updates
-   Roadmap generation
-   GEMS task completion
-   Internship application
-   Internship evaluation
-   Mentor registration
-   Mentor verification
-   Mentorship request
-   Mentorship session
-   Mentor feedback
-   Document upload
-   Document verification
-   Achievement creation

------------------------------------------------------------------------

# 19. Success Metrics

## Student Development

-   Assessment completion
-   Skill-gap reduction
-   Roadmap completion
-   GEMS task completion
-   Learning completion

## Internship

-   Internship applications
-   Application progression
-   Internship completion
-   Industry evaluations

## Mentorship

-   Registered mentors
-   Verified mentors
-   Mentor-student connections
-   Mentorship requests
-   Completed sessions
-   Mentor feedback
-   Student mentorship activity

## Engagement

-   Training participation
-   Workshop participation
-   Competition participation
-   Community contributions

## Career Growth

-   Verified skills
-   Portfolio completeness
-   Resume readiness
-   Certifications
-   Internship experience
-   Job / placement applications

------------------------------------------------------------------------

# 20. Final Product Definition

The Student Module is one connected career-development lifecycle:

``` text
UNDERSTAND THE STUDENT
        ↓
ASSESS THE STUDENT
        ↓
IDENTIFY THE GAP
        ↓
PLAN THE JOURNEY
        ↓
EXECUTE THE JOURNEY
        ↓
GET REAL-WORLD EXPOSURE
        ↓
GET GUIDANCE & MENTORSHIP
        ↓
COLLECT VERIFIED EVIDENCE
        ↓
BUILD CAREER PROFILE
        ↓
REASSESS & IMPROVE
```

## Core Intelligence Loop

``` text
ASSESS
   ↓
ANALYZE
   ↓
PLAN
   ↓
GEMS
   ↓
LEARN
   ↓
PRACTICE
   ↓
EXPERIENCE
   ↓
MENTOR
   ↓
EVALUATE
   ↓
VERIFY
   ↓
REASSESS
   ↓
IMPROVE
```

**Final Student Module: 7 integrated major features.**

GEMS remains inside **Achiever AI**, while mentorship is an integrated
part of **Training, Workshops, Mentorship & Student Engagement** and
supports an open mentor-registration model for faculty, seniors, alumni,
developers, industry professionals and other qualified mentors.
