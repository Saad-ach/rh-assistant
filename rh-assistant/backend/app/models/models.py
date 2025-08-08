from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # e.g., "user", "admin", "hr"


class HRDocument(Base):
    __tablename__ = "hr_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    source = Column(String)
    category = Column(String, index=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HRValidation(Base):
    __tablename__ = "hr_validations"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text)
    proposed_response = Column(Text)
    confidence_score = Column(Integer)
    hr_feedback = Column(Text, nullable=True)
    approved = Column(Boolean, nullable=True)  # True, False, or None (pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    validated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True) 