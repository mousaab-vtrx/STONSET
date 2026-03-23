"""Department (Département) Model."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Department(SQLModel, table=True):
    """Department ORM Model.
    
    Represents academic departments/faculties.
    From diagrams: Figure 7 - Département
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_department: str = Field(index=True, description="Department name")
    description: Optional[str] = None
    
    # Foreign key for department head (Chef de département)
    chef_department_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    chef_department: Optional["User"] = Relationship(back_populates="departments_headed")
    niveaux: list["Niveau"] = Relationship(back_populates="department")
