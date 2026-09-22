from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import schemas, models
from app.core.config import settings # Import settings
from app.services import hr_service
from app.services.document_index import index_answer
from .chat import get_current_user # Import get_current_user from chat.py

router = APIRouter()

async def get_current_admin_user(current_user: schemas.User = Depends(get_current_user)):
    # Allow admin@example.com by convention in dev
    if (
        getattr(current_user, "role", "user") == "admin"
        or getattr(current_user, "email", "") in {"admin", "admin@example.com", "admin@eubia.de"}
    ):
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")


@router.get("/stats", response_model=dict)
async def get_admin_stats(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_admin_user)):
    total_users = db.query(models.User).count()
    total_documents = db.query(models.DocumentRecord).count()
    try:
        pending_validations = db.query(models.HRQuestion).filter(
            models.HRQuestion.status == "pending"
        ).count()
    except Exception:
        # Validation tables are optional in the lightweight demo schema.
        pending_validations = 0
    return {
        "total_users": total_users,
        "total_documents": total_documents,
        "pending_validations": pending_validations,
    }


@router.get("/documents", response_model=List[schemas.DocumentRecordResponse])
async def get_documents(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_admin_user),
):
    return (
        db.query(models.DocumentRecord)
        .order_by(models.DocumentRecord.created_at.desc())
        .all()
    )


@router.get("/questions", response_model=List[dict])
async def get_questions(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_admin_user),
):
    questions = (
        db.query(models.HRQuestion)
        .filter(models.HRQuestion.status == "pending")
        .order_by(models.HRQuestion.created_at.asc())
        .all()
    )
    return [
        {
            "id": item.id,
            "query": item.question,
            "proposed_response": item.proposed_response,
            "confidence_score": item.confidence_score,
            "hr_feedback": item.answer,
            "approved": None,
            "status": item.status,
        }
        for item in questions
    ]


@router.get("/validations/pending", response_model=List[schemas.HRValidationInDB])
async def get_pending_validations(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_admin_user)):
    questions = (
        db.query(models.HRQuestion)
        .filter(models.HRQuestion.status == "pending")
        .order_by(models.HRQuestion.created_at.asc())
        .all()
    )
    return [
        {
            "id": item.id,
            "query": item.question,
            "proposed_response": item.proposed_response,
            "confidence_score": item.confidence_score,
            "hr_feedback": item.answer,
            "approved": None,
        }
        for item in questions
    ]


@router.post("/validate/{validation_id}", response_model=schemas.HRValidationInDB)
async def validate_hr_response(
    validation_id: int,
    approved: bool,
    hr_feedback: str | None = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_admin_user),
):
    question = db.query(models.HRQuestion).filter(models.HRQuestion.id == validation_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if approved and not (hr_feedback or "").strip():
        raise HTTPException(status_code=422, detail="An administrator answer is required")
    question.answer = hr_feedback.strip() if hr_feedback else None
    question.status = "answered" if approved else "rejected"
    question.answered_by = getattr(current_user, "email", "admin")
    question.answered_at = datetime.utcnow()
    db.commit()
    if approved:
        await index_answer(
            f"answer-{question.id}",
            question.question,
            question.answer or "",
            {
                "filename": f"EUBIA_ADMIN_ANSWER_{question.id}",
                "category": "validated-hr-answers",
                "language": "de-fr",
                "source": "admin-validated",
            },
        )
    return {
        "id": question.id,
        "query": question.question,
        "proposed_response": question.proposed_response,
        "confidence_score": question.confidence_score,
        "hr_feedback": question.answer,
        "approved": approved,
    }
