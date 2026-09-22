"""Populate the local EUBIA demo database and semantic index.

Run from backend:
    .venv\\Scripts\\python.exe scripts\\seed_demo_database.py
"""

import asyncio
import hashlib
import sys
from pathlib import Path

from sqlalchemy import select

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.data.eubia_demo_documents import DEMO_DOCUMENTS
from app.database import Base, SessionLocal, engine
from app.models import models
from app.services.document_index import index_document


async def seed() -> None:
    Base.metadata.create_all(
        bind=engine,
        tables=[
            models.User.__table__,
            models.DocumentRecord.__table__,
            models.HRQuestion.__table__,
        ],
    )

    inserted = 0
    indexed = 0
    with SessionLocal() as db:
        for item in DEMO_DOCUMENTS:
            content_hash = hashlib.sha256(item["content"].encode("utf-8")).hexdigest()
            existing = db.scalar(
                select(models.DocumentRecord).where(
                    models.DocumentRecord.content_hash == content_hash
                )
            )
            if existing:
                document_id = existing.id
            else:
                record = models.DocumentRecord(
                    filename=item["filename"],
                    category=item["category"],
                    language=item["language"],
                    blob_name=f"demo/{item['filename']}",
                    content_hash=content_hash,
                    extracted_text=item["content"],
                    source=item.get("source", f"synthetic://eubia-demo/{item['filename']}"),
                    status="indexed",
                    uploaded_by="demo-seed",
                )
                db.add(record)
                db.commit()
                db.refresh(record)
                document_id = record.id
                inserted += 1

            await index_document(
                f"demo-{document_id}",
                item["content"],
                {
                    "filename": item["filename"],
                    "category": item["category"],
                    "language": item["language"],
                    "source": item.get("source", f"synthetic://eubia-demo/{item['filename']}"),
                },
            )
            indexed += 1

    print(f"Inserted {inserted} new synthetic documents.")
    print(f"Indexed {indexed} documents for semantic search.")
    print("Reminder: this corpus is fictional and must not be used as real HR policy.")


if __name__ == "__main__":
    asyncio.run(seed())
