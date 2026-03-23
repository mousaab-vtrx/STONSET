"""Logiciel Schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class LogicielBase(BaseModel):
    """Base schema for software."""
    nom_logiciel: str = Field(..., description="Software name")
    version: Optional[str] = None
    description: Optional[str] = None
    systeme_id: int


class LogicielCreate(LogicielBase):
    """Schema for creating software."""
    pass


class LogicielUpdate(BaseModel):
    """Schema for updating software."""
    nom_logiciel: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None


class LogicielResponse(LogicielBase):
    """Schema for software response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
