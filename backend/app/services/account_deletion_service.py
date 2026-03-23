"""Account deletion service with feedback collection."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.account_deletion_feedback import AccountDeletionFeedback


class AccountDeletionService:
    """Service for managing account deletion and collecting feedback."""

    @staticmethod
    async def save_deletion_feedback(
        session: AsyncSession,
        user_id: int,
        reason: str,
        additional_feedback: Optional[str] = None
    ) -> AccountDeletionFeedback:
        """
        Save user feedback before account deletion.

        Args:
            session: Async database session
            user_id: ID of user deleting their account
            reason: Predefined reason for deletion
            additional_feedback: Optional additional feedback from user

        Returns:
            Created feedback record
        """
        feedback = AccountDeletionFeedback(
            user_id=user_id,
            reason=reason,
            additional_feedback=additional_feedback
        )
        session.add(feedback)
        await session.flush()  # Flush to DB, caller handles commit
        await session.refresh(feedback)  # Refresh to get generated ID
        return feedback

    @staticmethod
    async def delete_user_account(
        session: AsyncSession,
        user_id: int
    ) -> bool:
        """
        Delete user account and all associated data.

        Args:
            session: Async database session
            user_id: ID of user to delete

        Returns:
            True if deletion successful, False otherwise
        """
        try:
            # Query user asynchronously
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()

            if not user:
                return False

            # Delete user (cascade delete will handle related records)
            await session.delete(user)
            await session.flush()  # Flush deletion, caller handles commit
            return True

        except Exception as e:
            await session.rollback()
            print(f"Error deleting user account: {e}")
            return False

    @staticmethod
    def get_deletion_reasons() -> list[str]:
        """Get list of predefined deletion reasons. (Sync - no DB calls)"""
        return [
            "Privacy concerns",
            "App is not useful",
            "Technical issues",
            "Switching to another service",
            "Other"
        ]
