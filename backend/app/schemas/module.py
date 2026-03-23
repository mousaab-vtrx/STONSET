"""Module Schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ModuleBase(BaseModel):
    """Base schema for course/module."""
    code_module: str = Field(..., description="Course code")
    nom_module: str = Field(..., description="Course name")
    semestre_module: Optional[str] = None
    description: Optional[str] = None
    filiere_id: int


class ModuleCreate(ModuleBase):
    """Schema for creating course/module."""
    pass


class ModuleUpdate(BaseModel):
    """Schema for updating course/module."""
    code_module: Optional[str] = None
    nom_module: Optional[str] = None
    semestre_module: Optional[str] = None
    description: Optional[str] = None


class ModuleResponse(ModuleBase):
    """Schema for course/module response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
