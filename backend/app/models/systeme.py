"""Système (Operating System) Model."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Systeme(SQLModel, table=True):
    """Operating System ORM Model.
    
    Represents operating systems available in TP rooms.
    From diagrams: Figure 7 - Système
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_systeme: str = Field(index=True, unique=True, description="OS name (e.g., 'Windows 10', 'Linux Ubuntu')")
    version: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    logiciels: list["Logiciel"] = Relationship(back_populates="systeme")
    salles_tp: list["SalleTP"] = Relationship(back_populates="systeme")
