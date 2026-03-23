"""État (Status) Model."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Etat(SQLModel, table=True):
    """Status/State ORM Model.
    
    Represents possible states for reservations (e.g., Pending, Approved, Rejected).
    From diagrams: Figure 7 - État
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_etat: str = Field(index=True, unique=True, description="Status name (e.g., 'Pending', 'Approved')")
    description: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    reservations: list["Reservation"] = Relationship(back_populates="etat")
