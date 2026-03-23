"""
User ORM model.
Base model for Enseignant, Chef de département, and Responsable du service.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    """
    User model - Base class for all user types.
    
    Represents: Enseignant, Chef de département, Responsable du service
    From diagrams: Figure 1, Figure 2, Figure 3
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    nom_user: str = Field(max_length=255)
    prenom_user: str = Field(default="", max_length=255)
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    user_type: str = Field(default="enseignant", max_length=50)  # enseignant, chef_dept, responsable_service
    management_code: Optional[str] = Field(default=None, unique=True, index=True, max_length=50)  # Unique code for managers to share with subordinates
    supervisor_id: Optional[int] = Field(default=None, foreign_key="user.id")  # FK to manager (if this user is managed)
    avatar_url: Optional[str] = Field(default=None, max_length=500)  # URL to user's avatar image
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    reservations: list["Reservation"] = Relationship(back_populates="enseignant")
    departments_headed: list["Department"] = Relationship(back_populates="chef_department")
    supervisor: Optional["User"] = Relationship(
        back_populates="subordinates",
        sa_relationship_kwargs={"remote_side": "User.id", "foreign_keys": "User.supervisor_id"}
    )
    subordinates: list["User"] = Relationship(back_populates="supervisor")
