"""Niveau Repository."""
from sqlmodel import Session, select
from app.models.niveau import Niveau
from app.repositories.base import BaseRepository


class NiveauRepository(BaseRepository[Niveau]):
    """Repository for Niveau (Academic Level) entity."""
    
    async def get_by_department(self, session: Session, department_id: int) -> list[Niveau]:
        """Get all levels in a department."""
        query = select(Niveau).where(Niveau.department_id == department_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_name(self, session: Session, name: str) -> Niveau | None:
        """Get level by name."""
        query = select(Niveau).where(Niveau.nom_niveau == name)
        result = await session.execute(query)
        return result.scalars().first()
