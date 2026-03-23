"""SalleTP (TP Room/Lab) Model."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class SalleTP(SQLModel, table=True):
    """TP Room/Laboratory ORM Model.
    
    Represents physical rooms/laboratories available for reservation.
    From diagrams: Figure 7 - SalleTP
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_salle: str = Field(index=True, description="Room name")
    code: Optional[str] = Field(default=None, index=True, description="Room code (e.g., L101)")
    capacite: int = Field(description="Student capacity")
    access_internet: bool = Field(default=False, description="Has internet access")
    equipement_reseau: bool = Field(default=False, description="Has network equipment")
    videoprojecteur: bool = Field(default=False, description="Has projector")
    description: Optional[str] = None
    
    # Foreign key
    systeme_id: int = Field(foreign_key="systeme.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    
    # Relationships
    systeme: "Systeme" = Relationship(back_populates="salles_tp")
    reservations: list["Reservation"] = Relationship(back_populates="salle_tp")
