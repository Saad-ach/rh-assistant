from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import schemas, models
from app.core.config import settings # Import settings
from app.services import hr_service
from .chat import get_current_user # Import get_current_user from chat.py

router = APIRouter()

async def get_current_admin_user(current_user: schemas.User = Depends(get_current_user)):
    # Allow admin@example.com by convention in dev
    if getattr(current_user, "role", "user") == "admin" or getattr(current_user, "email", "") == "admin@example.com":
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")


@router.get("/stats", response_model=dict)
async def get_admin_stats(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_admin_user)):
    # Placeholder for admin statistics
    try:
        total_users = db.query(models.User).count()
        total_documents = db.query(models.HRDocument).count()
        pending_validations = db.query(models.HRValidation).filter(models.HRValidation.approved.is_(None)).count()
        return {
            "total_users": total_users,
            "total_documents": total_documents,
            "pending_validations": pending_validations,
        }
    except Exception:
        # Dev fallback stats
        return {
            "total_users": 1,
            "total_documents": 0,
            "pending_validations": 0,
        }


@router.get("/validations/pending", response_model=List[schemas.HRValidationInDB])
async def get_pending_validations(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_admin_user)):
    try:
        validations = hr_service.get_pending_validations(db)
        return validations
    except Exception:
        return []


@router.post("/validate/{validation_id}", response_model=schemas.HRValidationInDB)
async def validate_hr_response(
    validation_id: int,
    approved: bool,
    hr_feedback: str | None = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_admin_user),
):
    try:
        validation = hr_service.update_hr_validation_status(db, validation_id, approved, hr_feedback)
        if not validation:
            raise HTTPException(status_code=404, detail="Validation not found")
        return validation
    except Exception:
        raise HTTPException(status_code=503, detail="Validation service unavailable in dev mode")
