import asyncio
from datetime import datetime, timezone
import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import Student, GemsDailyPlan

logger = logging.getLogger(__name__)

async def reminder_loop():
    while True:
        try:
            db = SessionLocal()
            try:
                now = datetime.now(timezone.utc)
                current_time_str = now.strftime("%H:%M")
                
                # Fetch students with reminders enabled and time matching current minute
                # In a real app, this should track last_sent_date to avoid duplicates
                students = db.query(Student).filter(
                    Student.gems_reminder_enabled == True,
                    Student.gems_reminder_time == current_time_str
                ).all()
                
                for student in students:
                    # Check if they have an active daily plan
                    plan = db.query(GemsDailyPlan).filter(
                        GemsDailyPlan.student_id == student.id,
                        GemsDailyPlan.plan_date == now.date()
                    ).first()
                    
                    if plan and plan.status == "active":
                        print(f"\n[GEMS REMINDER MOCK] Sending reminder to {student.user.email} (Student ID: {student.id})")
                        print(f"\"Your SKILLY daily plan is ready. Today's Plan ID: {plan.id}. Time to Learn -> Practice -> Review!\"\n")
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error in reminder loop: {e}")
            
        # Sleep for 60 seconds
        await asyncio.sleep(60)

def start_reminder_service():
    asyncio.create_task(reminder_loop())
