"""Section (Class Group) Model."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Section(SQLModel, table=True):
    """Class Group/Section ORM Model.
    
    Represents student groups/sections for a specific module.
    From diagrams: Figure 7 - Section
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_section: str = Field(description="Section name")
    numero_section: int = Field(description="Section number")
    capacity: Optional[int] = None
    
    # Foreign key
    module_id: int = Field(foreign_key="module.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    module: "Module" = Relationship(back_populates="sections")
    groupes_tp: list["GroupeTP"] = Relationship(back_populates="section")
