"""Logiciel Repository."""
from sqlmodel import Session, select
from app.models.logiciel import Logiciel
from app.repositories.base import BaseRepository


class LogicielRepository(BaseRepository[Logiciel]):
    """Repository for Logiciel (Software) entity."""
    
    async def get_by_systeme(self, session: Session, systeme_id: int) -> list[Logiciel]:
        """Get all software for an OS."""
        query = select(Logiciel).where(Logiciel.systeme_id == systeme_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_name(self, session: Session, name: str) -> list[Logiciel]:
        """Get software by name (may appear on multiple OS)."""
        query = select(Logiciel).where(Logiciel.nom_logiciel == name)
        result = await session.execute(query)
        return result.scalars().all()
