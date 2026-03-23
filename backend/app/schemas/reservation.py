"""Réservation Schemas."""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field


class ReservationBase(BaseModel):
    """Base schema for reservation."""
    date_seance: date = Field(..., description="Date of the session")
    access_internet: bool = Field(default=False)
    equipement_reseau: bool = Field(default=False)
    videoprojecteur: bool = Field(default=False)
    type_reservation: str = Field(default="TP", description="Type: TP, Exam, Lecture, etc.")
    notes: Optional[str] = None
    enseignant_id: int
    salle_tp_id: int
    creneau_id: int
    etat_id: int
    groupe_tp_id: int
    vacances_id: Optional[int] = None


class ReservationCreate(ReservationBase):
    """Schema for creating reservation."""
    pass


class ReservationUpdate(BaseModel):
    """Schema for updating reservation."""
    date_seance: Optional[date] = None
    access_internet: Optional[bool] = None
    equipement_reseau: Optional[bool] = None
    videoprojecteur: Optional[bool] = None
    type_reservation: Optional[str] = None
    notes: Optional[str] = None
    etat_id: Optional[int] = None
    vacances_id: Optional[int] = None


class ReservationResponse(ReservationBase):
    """Schema for reservation response - without nested relationships to avoid lazy-loading issues."""
    id: int
    date_demande: datetime
    date_reponse: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
