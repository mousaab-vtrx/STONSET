"""Vacances Schemas."""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field


class VacancesBase(BaseModel):
    """Base schema for vacation period."""
    nom_vacances: str = Field(..., description="Vacation name")
    date_debut: date = Field(..., description="Start date")
    date_fin: date = Field(..., description="End date")
    description: Optional[str] = None


class VacancesCreate(VacancesBase):
    """Schema for creating vacation period."""
    pass


class VacancesUpdate(BaseModel):
    """Schema for updating vacation period."""
    nom_vacances: Optional[str] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    description: Optional[str] = None


class VacancesResponse(VacancesBase):
    """Schema for vacation period response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
