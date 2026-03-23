"""
User repository - Data access for User model.
"""
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """User repository - CRUD operations for users."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository."""
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_by_management_code(self, management_code: str) -> Optional[User]:
        """Get user by management code."""
        statement = select(User).where(User.management_code == management_code)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all active users."""
        statement = select(User).where(User.is_active == True).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    # TODO: Add more user-specific query methods as needed from diagrams
    # Example:
    # async def get_users_by_department(self, department_id: int) -> list[User]:
    #     """Get users by department."""
    #     ...
