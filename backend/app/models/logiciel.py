"""Logiciel (Software) Model."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Logiciel(SQLModel, table=True):
    """Software/Application ORM Model.
    
    Represents software applications available on systems.
    From diagrams: Figure 7 - Logiciel
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_logiciel: str = Field(index=True, description="Software name")
    version: Optional[str] = None
    description: Optional[str] = None
    
    # Foreign key
    systeme_id: int = Field(foreign_key="systeme.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    systeme: "Systeme" = Relationship(back_populates="logiciels")
