"""GroupeTP Schemas - Supports multiple session types (CM, TD, TP, EXAM, SEMINAR)."""
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


# Session types
SESSION_TYPES = Literal["CM", "TD", "TP", "EXAM", "SEMINAR"]


class GroupeTPBase(BaseModel):
    """Base schema for TP group - supports multiple session types.
    
    Type options:
    - CM: Course magistral (lectures)
    - TD: Travaux dirigés (tutorials)
    - TP: Travaux pratiques (labs/practical work)
    - EXAM: Examinations
    - SEMINAR: Seminars/workshops
    """
    num_groupe: int = Field(..., description="Group number")
    nom_groupe: Optional[str] = None
    capacity: Optional[int] = None
    type: SESSION_TYPES = Field(default="TP", description="Session type: CM, TD, TP, EXAM, or SEMINAR")
    module_id: int
    section_id: int


class GroupeTPCreate(GroupeTPBase):
    """Schema for creating TP group."""
    pass


class GroupeTPUpdate(BaseModel):
    """Schema for updating TP group."""
    num_groupe: Optional[int] = None
    nom_groupe: Optional[str] = None
    capacity: Optional[int] = None
    type: Optional[SESSION_TYPES] = None


class GroupeTPResponse(GroupeTPBase):
    """Schema for TP group response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
