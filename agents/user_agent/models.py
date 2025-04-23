"""
User Agent Models Module

Module chứa các model cho User Agent
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user model."""
    
    email: EmailStr
    fullname: str


class UserCreate(UserBase):
    """Model for user creation."""
    
    password: str


class UserUpdate(BaseModel):
    """Model for user update."""
    
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    """User model."""
    
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_premium: bool
    quota_remaining: int
    
    class Config:
        orm_mode = True


class TokenData(BaseModel):
    """Token data model."""
    
    username: str
    exp: Optional[int] = None


class Token(BaseModel):
    """Authentication token model."""
    
    access_token: str
    token_type: str
    user: User


class ApiKeyCreate(BaseModel):
    """Model for API key creation."""
    
    name: str
    expires_at: Optional[datetime] = None


class ApiKey(BaseModel):
    """API key model."""
    
    id: str
    key: str
    name: str
    user_id: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    is_active: bool 