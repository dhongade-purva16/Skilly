from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from seed import seed_db
from app.services.reminder import start_reminder_service

# Create tables and seed data
Base.metadata.create_all(bind=engine)
try:
    seed_db()
except Exception as e:
    print(f"Startup seed notice: {e}")

from app.api.v1.api import api_router

import sys

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if "pytest" not in sys.modules:
        start_reminder_service()
    yield
    # Shutdown
    pass

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to SKILLY API - Student Phase 1"}

