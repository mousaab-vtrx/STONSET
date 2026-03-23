"""Filière Repository."""
from sqlmodel import Session, select
from app.models.filiere import Filiere
from app.repositories.base import BaseRepository


class FiliereRepository(BaseRepository[Filiere]):
    """Repository for Filière (Academic Program) entity."""
    
    async def get_by_niveau(self, session: Session, niveau_id: int) -> list[Filiere]:
        """Get all programs in a level."""
        query = select(Filiere).where(Filiere.niveau_id == niveau_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_name(self, session: Session, name: str) -> Filiere | None:
        """Get program by name."""
        query = select(Filiere).where(Filiere.nom_filiere == name)
        result = await session.execute(query)
        return result.scalars().first()
