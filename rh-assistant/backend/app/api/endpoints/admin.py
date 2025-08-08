from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import schemas, models
from app.services import hr_service
from .chat import get_current_user # Import get_current_user from chat.py

router = APIRouter()

async def get_current_admin_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user


@router.get("/stats", response_model=dict)
async def get_admin_stats(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_admin_user)):
    # Placeholder for admin statistics
    total_users = db.query(models.User).count()
    total_documents = db.query(models.HRDocument).count()
    pending_validations = db.query(models.HRValidation).filter(models.HRValidation.approved.is_(None)).count()
    return {
        "total_users": total_users,
        "total_documents": total_documents,
        "pending_validations": pending_validations,
    }


@router.get("/validations/pending", response_model=List[schemas.HRValidationInDB])
async def get_pending_validations(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_admin_user)):
    validations = hr_service.get_pending_validations(db)
    return validations


@router.post("/validate/{validation_id}", response_model=schemas.HRValidationInDB)
async def validate_hr_response(
    validation_id: int,
    approved: bool,
    hr_feedback: str | None = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_admin_user),
):
    validation = hr_service.update_hr_validation_status(db, validation_id, approved, hr_feedback)
    if not validation:
        raise HTTPException(status_code=404, detail="Validation not found")
    return validation
