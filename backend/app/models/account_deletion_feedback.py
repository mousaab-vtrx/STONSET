"""Account Deletion Feedback Model."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class AccountDeletionFeedback(SQLModel, table=True):
    """Model for storing user account deletion feedback."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="user.id",
        description="User who deleted their account"
    )
    reason: str = Field(
        max_length=100,
        description="Predefined reason for deletion (e.g., Privacy concerns, App is not useful, etc.)"
    )
    additional_feedback: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Additional user-provided feedback or explanation"
    )
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
