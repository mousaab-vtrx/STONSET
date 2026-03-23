"""Système Schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SystemeBase(BaseModel):
    """Base schema for operating system."""
    nom_systeme: str = Field(..., description="OS name")
    version: Optional[str] = None


class SystemeCreate(SystemeBase):
    """Schema for creating operating system."""
    pass


class SystemeUpdate(BaseModel):
    """Schema for updating operating system."""
    nom_systeme: Optional[str] = None
    version: Optional[str] = None


class SystemeResponse(SystemeBase):
    """Schema for operating system response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
