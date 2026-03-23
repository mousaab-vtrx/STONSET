"""Section Schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SectionBase(BaseModel):
    """Base schema for section."""
    nom_section: str = Field(..., description="Section name")
    numero_section: int = Field(..., description="Section number")
    capacity: Optional[int] = None
    module_id: int


class SectionCreate(SectionBase):
    """Schema for creating section."""
    pass


class SectionUpdate(BaseModel):
    """Schema for updating section."""
    nom_section: Optional[str] = None
    numero_section: Optional[int] = None
    capacity: Optional[int] = None


class SectionResponse(SectionBase):
    """Schema for section response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
