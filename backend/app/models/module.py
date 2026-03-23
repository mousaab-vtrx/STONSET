"""Module (Course/Subject) Model."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Module(SQLModel, table=True):
    """Course/Subject ORM Model.
    
    Represents academic courses/modules.
    From diagrams: Figure 7 - Module
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    code_module: str = Field(index=True, unique=True, description="Course code")
    nom_module: str = Field(index=True, description="Course name")
    semestre_module: Optional[str] = None  # Semester (S1, S2, etc.)
    description: Optional[str] = None
    
    # Foreign key
    filiere_id: int = Field(foreign_key="filiere.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    filiere: "Filiere" = Relationship(back_populates="modules")
    sections: list["Section"] = Relationship(back_populates="module")
    groupes_tp: list["GroupeTP"] = Relationship(back_populates="module")
