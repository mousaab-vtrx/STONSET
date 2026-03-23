"""Filière (Program/Major) Model."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Filiere(SQLModel, table=True):
    """Academic Program/Major ORM Model.
    
    Represents academic programs/specializations (e.g., Informatique, Génie Civil).
    From diagrams: Figure 7 - Filière
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_filiere: str = Field(index=True, description="Program name")
    description: Optional[str] = None
    
    # Foreign key
    niveau_id: int = Field(foreign_key="niveau.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    niveau: "Niveau" = Relationship(back_populates="filieres")
    modules: list["Module"] = Relationship(back_populates="filiere")
