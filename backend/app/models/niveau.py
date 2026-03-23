"""Niveau (Academic Level/Year) Model."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Niveau(SQLModel, table=True):
    """Academic Level/Year ORM Model.
    
    Represents academic levels (e.g., 1st year, 2nd year, 3rd year).
    From diagrams: Figure 7 - Niveau
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_niveau: str = Field(index=True, description="Level name (e.g., '1ère année', '2ème année')")
    arch_niveau: Optional[str] = None  # Architecture/category
    not_semestre: Optional[str] = None  # Semester notation
    
    # Foreign key
    department_id: int = Field(foreign_key="department.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    department: "Department" = Relationship(back_populates="niveaux")
    filieres: list["Filiere"] = Relationship(back_populates="niveau")
