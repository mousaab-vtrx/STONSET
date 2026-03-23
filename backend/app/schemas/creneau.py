"""Créneau Schemas."""
from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, Field


class CreneauBase(BaseModel):
    """Base schema for time slot."""
    heure_debut: time = Field(..., description="Start time")
    duree: int = Field(..., description="Duration in minutes")
    num_jour: int = Field(..., description="Day number (1-7)")
    num_semaine: int = Field(..., description="Week number (1-52)")
    jour_nom: Optional[str] = None


class CreneauCreate(CreneauBase):
    """Schema for creating time slot."""
    pass


class CreneauUpdate(BaseModel):
    """Schema for updating time slot."""
    heure_debut: Optional[time] = None
    duree: Optional[int] = None
    num_jour: Optional[int] = None
    num_semaine: Optional[int] = None
    jour_nom: Optional[str] = None


class CreneauResponse(CreneauBase):
    """Schema for time slot response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
