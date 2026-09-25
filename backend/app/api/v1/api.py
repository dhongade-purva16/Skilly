from fastapi import APIRouter

from app.api.v1.endpoints import student, career, skill, assessment, company, student_jobs

api_router = APIRouter()
api_router.include_router(student.router, prefix="/student", tags=["student"])
api_router.include_router(career.router, prefix="/career-goal", tags=["career-goal"])
api_router.include_router(skill.router, prefix="/skills", tags=["skills"])
api_router.include_router(assessment.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(company.router, prefix="/company", tags=["company"])
api_router.include_router(student_jobs.router, prefix="/student", tags=["student_jobs"])
