from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Date, Float, ForeignKey, LargeBinary, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base

# Define a custom type for VECTOR if pgvector is used, otherwise use ARRAY or JSONB for compatibility
# For pgvector, you would typically import it: from pgvector.sqlalchemy import Vector
# Since we don't have pgvector directly, we'll use a placeholder or ensure it's handled by JSONB
# For simplicity and broad compatibility without installing pgvector, we'll map VECTOR to JSONB for now.
# If you integrate pgvector, you'll replace this with the actual Vector type.
# For now, let's assume `VECTOR` from your schema can be mapped to a JSONB in SQLAlchemy to hold the array of floats.
# You would need to add 'from sqlalchemy.types import TypeDecorator, Float' and define a custom Vector type
# if pgvector is not used and you want to ensure specific behavior for vector storage.
# For direct pgvector integration, you would typically use:
# from pgvector.sqlalchemy import Vector
# embedding_vector = Column(Vector(1536))

# For UUID and ARRAY, we need to ensure sqlalchemy-utils is installed or define custom types if not using PostgreSQL specific dialects.
# Assuming PostgreSQL dialect is active and supports UUID and ARRAY from sqlalchemy.dialects.postgresql.

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # e.g., "user", "admin", "hr"


class Collaborator(Base):
    __tablename__ = "collaborators"
    collaborator_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    department = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    hire_date = Column(Date, nullable=False)
    contract_type = Column(String(50))
    manager_id = Column(Integer, ForeignKey("collaborators.collaborator_id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Self-referencing relationship for managers
    manager = relationship("Collaborator", remote_side=[collaborator_id], backref="direct_reports")
    chat_interactions = relationship("ChatInteraction", back_populates="collaborator")
    hr_validations = relationship("HRValidation", back_populates="validator")


class QuestionCategory(Base):
    __tablename__ = "question_categories"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    description = Column(Text)
    priority = Column(Integer, default=3)  # CHECK constraint will be added by Alembic
    needs_approval = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    faq_questions = relationship("FAQQuestion", back_populates="category")


class FAQQuestion(Base):
    __tablename__ = "faq_questions"
    question_id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("question_categories.category_id"), nullable=False)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    keywords = Column(ARRAY(Text))  # PostgreSQL specific
    similarity_threshold = Column(Float, default=0.75)
    is_sensitive = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(String(100))

    category = relationship("QuestionCategory", back_populates="faq_questions")
    most_asked_in_metrics = relationship("PerformanceMetric", back_populates="most_asked_question")


class ChatInteraction(Base):
    __tablename__ = "chat_interactions"
    interaction_id = Column(Integer, primary_key=True, index=True)
    collaborator_id = Column(Integer, ForeignKey("collaborators.collaborator_id"))
    session_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False) # PostgreSQL specific UUID
    question_text = Column(Text, nullable=False)
    response_text = Column(Text)
    confidence_score = Column(Float)
    response_source = Column(String(50))
    is_approved = Column(Boolean, default=False)
    approved_by = Column(String(100))
    approval_date = Column(DateTime(timezone=True))
    needs_human_review = Column(Boolean, default=False)
    reviewed = Column(Boolean, default=False)
    feedback_score = Column(Integer) # CHECK constraint will be added by Alembic
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    response_time_ms = Column(Integer)
    # Using JSONB to store vector embeddings if pgvector is not directly integrated
    # If pgvector is installed, this would be: embedding_vector = Column(Vector(1536))
    embedding_vector = Column(JSONB) # Represents VECTOR(1536) in schema

    collaborator = relationship("Collaborator", back_populates="chat_interactions")
    hr_validations = relationship("HRValidation", back_populates="chat_interaction")


class HRDocument(Base):
    __tablename__ = "hr_documents"
    document_id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String(255), nullable=False)
    document_type = Column(String(50), nullable=False)
    file_path = Column(Text, nullable=False)
    file_hash = Column(LargeBinary, unique=True) # BYTEA in PostgreSQL
    original_text = Column(Text)
    processed_text = Column(Text)
    embedding_model = Column(String(50))
    is_active = Column(Boolean, default=True)
    validity_date = Column(Date)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    updated_by = Column(String(100))


class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"
    metric_id = Column(Integer, primary_key=True, index=True)
    metric_date = Column(Date, nullable=False)
    period = Column(String(10)) # CHECK constraint will be added by Alembic
    avg_response_time_ms = Column(Integer)
    accuracy_rate = Column(Float)
    system_availability = Column(Float)
    total_queries = Column(Integer)
    automated_responses = Column(Integer)
    human_reviews = Column(Integer)
    avg_feedback_score = Column(Float)
    unique_users = Column(Integer)
    most_asked_question_id = Column(Integer, ForeignKey("faq_questions.question_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    most_asked_question = relationship("FAQQuestion", back_populates="most_asked_in_metrics")


class HRValidation(Base):
    __tablename__ = "hr_validations"
    validation_id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)  # Ajout du champ query
    proposed_response = Column(Text, nullable=False)  # Ajout du champ proposed_response
    confidence_score = Column(Float, nullable=False)  # Ajout du champ confidence_score
    hr_feedback = Column(Text)  # Ajout du champ hr_feedback
    approved = Column(Boolean)  # Ajout du champ approved
    interaction_id = Column(Integer, ForeignKey("chat_interactions.interaction_id"))
    validator_id = Column(Integer, ForeignKey("collaborators.collaborator_id"))
    validation_result = Column(Boolean, nullable=False)
    comments = Column(Text)
    corrected_answer = Column(Text)
    validated_at = Column(DateTime(timezone=True), server_default=func.now())

    chat_interaction = relationship("ChatInteraction", back_populates="hr_validations")
    validator = relationship("Collaborator", back_populates="hr_validations")


class AuditLog(Base):
    __tablename__ = "audit_log"
    log_id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(50), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String(10), nullable=False) # CHECK constraint will be added by Alembic
    old_values = Column(JSONB) # JSONB for PostgreSQL
    new_values = Column(JSONB) # JSONB for PostgreSQL
    changed_by = Column(String(100))
    changed_at = Column(DateTime(timezone=True), server_default=func.now()) 