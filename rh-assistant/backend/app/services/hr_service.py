from sqlalchemy.orm import Session
from app.models import models, schemas
from app.ml.vectorizer import chroma_vectorizer
from app.ml.embeddings import embeddings_generator
from typing import List, Optional


def create_hr_document(db: Session, document: schemas.HRDocument):
    db_document = models.HRDocument(
        title=document.title,
        content=document.content,
        source=document.source,
        category=document.category,
        metadata=document.metadata,
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # Add document to ChromaDB
    doc_id = str(db_document.id)
    chroma_vectorizer.add_document(doc_id, document.content, document.metadata)
    return db_document


def search_hr_documents(query: str, n_results: int = 5):
    results = chroma_vectorizer.search_documents(query, n_results)
    return results


def create_hr_validation(db: Session, validation: schemas.HRValidationCreate):
    db_validation = models.HRValidation(
        query=validation.query,
        proposed_response=validation.proposed_response,
        confidence_score=validation.confidence_score,
        hr_feedback=validation.hr_feedback,
        approved=validation.approved,
    )
    db.add(db_validation)
    db.commit()
    db.refresh(db_validation)
    return db_validation


def get_pending_validations(db: Session) -> List[models.HRValidation]:
    return db.query(models.HRValidation).filter(models.HRValidation.approved.is_(None)).all()


def update_hr_validation_status(db: Session, validation_id: int, approved: bool, hr_feedback: Optional[str] = None):
    db_validation = db.query(models.HRValidation).filter(models.HRValidation.id == validation_id).first()
    if db_validation:
        db_validation.approved = approved
        db_validation.hr_feedback = hr_feedback
        db.commit()
        db.refresh(db_validation)
    return db_validation
