"""Créneau (Time Slot) Model."""
from datetime import datetime, time
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Creneau(SQLModel, table=True):
    """Time Slot ORM Model.
    
    Represents available time slots for room reservations.
    From diagrams: Figure 7 - Créneau
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    heure_debut: time = Field(description="Start time")
    duree: int = Field(description="Duration in minutes")
    num_jour: int = Field(description="Day number (1-7)")
    num_semaine: int = Field(description="Week number (1-52)")
    jour_nom: Optional[str] = None  # e.g., "Monday"
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    reservations: list["Reservation"] = Relationship(back_populates="creneau")
