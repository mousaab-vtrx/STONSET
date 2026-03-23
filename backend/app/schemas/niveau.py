"""Niveau Schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NiveauBase(BaseModel):
    """Base schema for academic level."""
    nom_niveau: str = Field(..., description="Level name")
    arch_niveau: Optional[str] = None
    not_semestre: Optional[str] = None
    department_id: int


class NiveauCreate(NiveauBase):
    """Schema for creating academic level."""
    pass


class NiveauUpdate(BaseModel):
    """Schema for updating academic level."""
    nom_niveau: Optional[str] = None
    arch_niveau: Optional[str] = None
    not_semestre: Optional[str] = None


class NiveauResponse(NiveauBase):
    """Schema for academic level response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
