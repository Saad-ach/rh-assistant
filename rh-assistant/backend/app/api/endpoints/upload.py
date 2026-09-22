from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
import docx
import hashlib
import io
import PyPDF2

from app.core.config import settings
from app.database import get_db
from app.models import models, schemas
from app.services.document_index import index_document
from app.services.document_storage import document_storage
from .chat import get_current_user

router = APIRouter()


@router.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    category: str = "general",
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    if (
        getattr(current_user, "role", "user") != "admin"
        and getattr(current_user, "email", "") not in {"admin", "admin@example.com", "admin@eubia.de"}
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    file_extension = (file.filename or "").rsplit(".", 1)[-1].lower()
    file_bytes = await file.read()

    if file_extension == "pdf":
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        extracted_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif file_extension in {"doc", "docx"}:
        document = docx.Document(io.BytesIO(file_bytes))
        extracted_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    else:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX documents are supported")

    if not extracted_text.strip():
        raise HTTPException(status_code=422, detail="The document contains no extractable text")

    content_hash = hashlib.sha256(file_bytes).hexdigest()
    blob_name = f"{category}/{content_hash}.{file_extension}"
    try:
        file_path = document_storage.save(blob_name, file_bytes, file.content_type)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    document = models.DocumentRecord(
        filename=file.filename or blob_name,
        category=category,
        language=settings.APP_DEFAULT_LANGUAGE,
        blob_name=blob_name,
        content_hash=content_hash,
        extracted_text=extracted_text,
        source=file_path,
        status="indexed",
        uploaded_by=getattr(current_user, "email", "admin"),
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    await index_document(
        str(document.id),
        extracted_text,
        {
            "source": file_path,
            "filename": document.filename,
            "category": category,
            "language": document.language,
        },
    )

    return {
        "filename": document.filename,
        "message": "Document uploaded, stored and indexed successfully",
        "document_id": document.id,
        "storage": file_path,
    }
