"""Etat Schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EtatBase(BaseModel):
    """Base schema for status."""
    nom_etat: str = Field(..., description="Status name")
    description: Optional[str] = None


class EtatCreate(EtatBase):
    """Schema for creating status."""
    pass


class EtatUpdate(BaseModel):
    """Schema for updating status."""
    nom_etat: Optional[str] = None
    description: Optional[str] = None


class EtatResponse(EtatBase):
    """Schema for status response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
