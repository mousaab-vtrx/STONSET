"""Système Repository."""
from sqlmodel import Session, select
from app.models.systeme import Systeme
from app.repositories.base import BaseRepository


class SystemeRepository(BaseRepository[Systeme]):
    """Repository for Système (Operating System) entity."""
    
    async def get_by_name(self, session: Session, name: str) -> Systeme | None:
        """Get OS by name."""
        query = select(Systeme).where(Systeme.nom_systeme == name)
        result = await session.execute(query)
        return result.scalars().first()
    
    async def get_all_systems(self, session: Session) -> list[Systeme]:
        """Get all available operating systems."""
        query = select(Systeme)
        result = await session.execute(query)
        return result.scalars().all()
