from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Generator
from firebase_admin import auth

from app.core.database import SessionLocal
from app.models import User
from app.core.security import init_firebase

init_firebase()

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        # For Phase 1 dev testing, if no token, create a mock user
        # IN PRODUCTION: raise HTTPException(status_code=401)
        mock_uid = "mock-firebase-uid-123"
        user = db.query(User).filter(User.firebase_uid == mock_uid).first()
        if not user:
            user = User(firebase_uid=mock_uid, email="mock@student.com")
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    token = authorization.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
    except ValueError:
        # Fallback for local development where firebase_admin lacks credentials
        import base64
        import json
        try:
            # Decode without verification for dev only
            payload = token.split('.')[1]
            # Add padding if needed
            payload += '=' * (-len(payload) % 4)
            decoded_token = json.loads(base64.urlsafe_b64decode(payload).decode('utf-8'))
            uid = decoded_token.get("user_id") or decoded_token.get("uid")
            email = decoded_token.get("email")
            if not uid:
                raise ValueError("No UID in token")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials (dev fallback failed: {e})",
            )
    except Exception as e:
        print("Firebase auth error:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = db.query(User).filter(User.firebase_uid == uid).first()
    if not user:
        user = User(firebase_uid=uid, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        
    return user

def get_current_student_user(user: User = Depends(get_current_user)) -> User:
    if user.user_type != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to student users",
        )
    return user

def get_current_hr_user(user: User = Depends(get_current_user)) -> User:
    if user.user_type != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to HR/Company users",
        )
    if not user.hr_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have an active HR profile",
        )
    return user
