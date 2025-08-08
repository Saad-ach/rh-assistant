from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class ChatQuery(BaseModel):
    message: str
    query_type: Optional[str] = "general"
    user_id: int
    session_id: str


class ChatResponse(BaseModel):
    response: str
    confidence_score: float
    sources: List[str]
    requires_validation: bool
    validation_status: Optional[str] = None
    response_time: float
    timestamp: datetime


class HRDocument(BaseModel):
    title: str
    content: str
    source: str
    category: str
    metadata: dict


class HRValidation(BaseModel):
    query: str
    proposed_response: str
    confidence_score: float
    hr_feedback: Optional[str] = None
    approved: Optional[bool] = None


class HRValidationCreate(HRValidation):
    pass


class HRValidationInDB(HRValidation):
    id: int

    class Config:
        from_attributes = True
