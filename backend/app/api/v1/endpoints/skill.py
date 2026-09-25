from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models import Skill, SkillCategory
from app.schemas.skill import SkillResponse, SkillCategoryResponse

router = APIRouter()

@router.get("/", response_model=List[SkillResponse])
def get_skills(db: Session = Depends(deps.get_db)):
    return db.query(Skill).all()

@router.get("/categories", response_model=List[SkillCategoryResponse])
def get_skill_categories(db: Session = Depends(deps.get_db)):
    return db.query(SkillCategory).all()
