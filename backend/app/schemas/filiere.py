"""Filière Schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FiliereBase(BaseModel):
    """Base schema for academic program."""
    nom_filiere: str = Field(..., description="Program name")
    description: Optional[str] = None
    niveau_id: int


class FiliereCreate(FiliereBase):
    """Schema for creating academic program."""
    pass


class FiliereUpdate(BaseModel):
    """Schema for updating academic program."""
    nom_filiere: Optional[str] = None
    description: Optional[str] = None


class FiliereResponse(FiliereBase):
    """Schema for academic program response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
