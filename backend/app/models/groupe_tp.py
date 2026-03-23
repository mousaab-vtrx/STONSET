"""GroupeTP (Group) Model - Supports multiple session types (CM, TD, TP, EXAM, SEMINAR)."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class GroupeTP(SQLModel, table=True):
    """Group ORM Model - represents groups for any session type.
    
    Supports multiple session types:
    - CM: Course magistral (lectures)
    - TD: Travaux dirigés (tutorials)
    - TP: Travaux pratiques (labs/practical work)
    - EXAM: Examinations
    - SEMINAR: Seminars/workshops
    
    From diagrams: Figure 7 - GroupeTP (extended for multiple types)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    num_groupe: int = Field(description="Group number")
    nom_groupe: Optional[str] = None
    capacity: Optional[int] = None
    
    # Session type - supports CM, TD, TP, EXAM, SEMINAR
    type: str = Field(
        default="TP",
        description="Session type: CM (lecture), TD (tutorial), TP (practical), EXAM (exam), SEMINAR (seminar)"
    )
    
    # Foreign keys
    module_id: int = Field(foreign_key="module.id")
    section_id: int = Field(foreign_key="section.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    module: "Module" = Relationship(back_populates="groupes_tp")
    section: "Section" = Relationship(back_populates="groupes_tp")
    reservations: list["Reservation"] = Relationship(back_populates="groupe_tp")
