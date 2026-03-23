"""
Base repository - CRUD operations wrapper.
Provides generic CRUD methods for all repositories.
"""
from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    """Generic repository for CRUD operations."""

    def __init__(self, session: AsyncSession, model: Type[T]):
        """Initialize repository."""
        self.session = session
        self.model = model

    async def create(self, session: AsyncSession, obj_in: SQLModel) -> T:
        """Create and return new object."""
        db_obj = self.model.from_orm(obj_in) if hasattr(obj_in, "dict") else self.model(**obj_in.dict())
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, session: AsyncSession, obj_id: int) -> Optional[T]:
        """Get object by ID."""
        statement = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(statement)
        return result.scalars().first()

    async def get_all(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> list[T]:
        """Get all objects with pagination."""
        statement = select(self.model).offset(skip).limit(limit)
        result = await session.execute(statement)
        return result.scalars().all()

    async def update(self, session: AsyncSession, obj_id: int, obj_in: SQLModel) -> Optional[T]:
        """Update object by ID."""
        db_obj = await self.get_by_id(session, obj_id)
        if not db_obj:
            return None
        
        update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, "dict") else obj_in
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, obj_id: int) -> bool:
        """Delete object by ID."""
        db_obj = await self.get_by_id(session, obj_id)
        if not db_obj:
            return False
        
        await session.delete(db_obj)
        await session.flush()
        return True

    async def commit(self) -> None:
        """Commit changes."""
        await self.session.commit()
