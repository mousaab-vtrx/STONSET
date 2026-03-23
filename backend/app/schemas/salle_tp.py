"""SalleTP Schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SalleTPBase(BaseModel):
    """Base schema for TP room."""
    nom_salle: str = Field(..., description="Room name")
    capacite: int = Field(..., description="Student capacity")
    access_internet: bool = Field(default=False)
    equipement_reseau: bool = Field(default=False)
    videoprojecteur: bool = Field(default=False)
    description: Optional[str] = None
    systeme_id: int


class SalleTPCreate(SalleTPBase):
    """Schema for creating TP room."""
    pass


class SalleTPUpdate(BaseModel):
    """Schema for updating TP room."""
    nom_salle: Optional[str] = None
    capacite: Optional[int] = None
    access_internet: Optional[bool] = None
    equipement_reseau: Optional[bool] = None
    videoprojecteur: Optional[bool] = None
    description: Optional[str] = None


class SalleTPResponse(SalleTPBase):
    """Schema for TP room response."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
