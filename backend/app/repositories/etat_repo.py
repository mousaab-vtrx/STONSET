"""Etat Repository."""
from sqlmodel import Session, select
from app.models.etat import Etat
from app.repositories.base import BaseRepository


class EtatRepository(BaseRepository[Etat]):
    """Repository for Etat (Status) entity."""
    
    async def get_by_name(self, session: Session, name: str) -> Etat | None:
        """Get status by name."""
        query = select(Etat).where(Etat.nom_etat == name)
        result = await session.execute(query)
        return result.scalars().first()
    
    async def get_all_statuses(self, session: Session) -> list[Etat]:
        """Get all available statuses."""
        query = select(Etat)
        result = await session.execute(query)
        return result.scalars().all()
