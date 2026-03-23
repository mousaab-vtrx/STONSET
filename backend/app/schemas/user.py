"""
User request/response schemas (Pydantic models).

Represents Enseignant, Chef de département, Responsable du service
From diagrams: Figure 1, Figure 2, Figure 3
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema - shared fields."""

    email: EmailStr
    nom_user: str = Field(..., min_length=1, max_length=255)
    prenom_user: str = Field(default="", max_length=255)
    user_type: str = Field(default="enseignant")  # enseignant, chef_dept, responsable_service


class UserCreate(UserBase):
    """User creation schema - for POST requests."""

    password: str = Field(..., min_length=8, max_length=255)
    management_code: Optional[str] = Field(None, max_length=50)  # Code to join under a manager


class UserUpdate(BaseModel):
    """User update schema - for PUT/PATCH requests."""

    email: Optional[EmailStr] = None
    nom_user: Optional[str] = Field(None, min_length=1, max_length=255)
    prenom_user: Optional[str] = Field(None, max_length=255)
    # TODO: Add other fields from diagrams
    # Note: password updates should use separate endpoint


class UserResponse(UserBase):
    """User response schema - for GET requests."""

    id: int
    is_active: bool
    avatar_url: Optional[str] = None
    management_code: Optional[str] = None
    supervisor_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class UserLoginRequest(BaseModel):
    """User login request schema."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: Optional[UserResponse] = None


class RefreshTokenRequest(BaseModel):
    """Refresh token request payload."""

    refresh_token: str
