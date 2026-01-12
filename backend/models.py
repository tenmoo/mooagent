from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    """User registration model."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr
    password: str


class User(BaseModel):
    """User model."""
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime
    is_active: bool = True


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data stored in JWT."""
    email: Optional[str] = None


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    conversation_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    conversation_id: Optional[str] = None
