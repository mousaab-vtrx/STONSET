"""Réservation (Reservation) Model."""
from datetime import datetime, date
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Reservation(SQLModel, table=True):
    """Reservation ORM Model.
    
    Represents room reservation requests from instructors.
    From diagrams: Figure 7 - Réservation (Core entity)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Date and time fields
    date_seance: date = Field(description="Date of the session/class")
    date_demande: datetime = Field(default_factory=datetime.utcnow, description="Request submission date")
    date_reponse: Optional[datetime] = None  # Response date (when approved/rejected)
    
    # Equipment requirements
    access_internet: bool = Field(default=False)
    equipement_reseau: bool = Field(default=False)
    videoprojecteur: bool = Field(default=False)
    type_reservation: str = Field(default="TP", description="Type: TP, Exam, Lecture, etc.")
    
    # Additional info
    notes: Optional[str] = None  # Additional notes/requirements
    
    # Foreign keys
    enseignant_id: int = Field(foreign_key="user.id", description="Instructor (Enseignant)")
    salle_tp_id: int = Field(foreign_key="salletp.id")
    creneau_id: int = Field(foreign_key="creneau.id")
    etat_id: int = Field(foreign_key="etat.id")
    groupe_tp_id: int = Field(foreign_key="groupetp.id")
    vacances_id: Optional[int] = Field(default=None, foreign_key="vacances.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    enseignant: "User" = Relationship(back_populates="reservations")
    salle_tp: "SalleTP" = Relationship(back_populates="reservations")
    creneau: "Creneau" = Relationship(back_populates="reservations")
    etat: "Etat" = Relationship(back_populates="reservations")
    groupe_tp: "GroupeTP" = Relationship(back_populates="reservations")
    vacances: Optional["Vacances"] = Relationship(back_populates="reservations")
