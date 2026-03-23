"""Vacances (Vacation/Break) Model."""
from datetime import datetime, date
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Vacances(SQLModel, table=True):
    """Vacation/Break Period ORM Model.
    
    Represents vacation periods when reservations are not available.
    From diagrams: Figure 7 - Vacances
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_vacances: str = Field(index=True, description="Vacation name (e.g., 'Été 2024')")
    date_debut: date = Field(description="Start date")
    date_fin: date = Field(description="End date")
    description: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    reservations: list["Reservation"] = Relationship(back_populates="vacances")
