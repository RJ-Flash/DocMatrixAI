from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user model."""
    email: Optional[EmailStr] = Field(None, description="User email")
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = Field(None, description="User full name")


class UserCreate(UserBase):
    """User creation model."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")
    full_name: str = Field(..., description="User full name")


class UserUpdate(BaseModel):
    """User update model."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    """User database model."""
    id: Optional[int] = None
    hashed_password: str = Field(..., description="Hashed password")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserResponse(UserBase):
    """User response model."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Token payload model."""
    sub: Optional[int] = None
    exp: Optional[datetime] = None