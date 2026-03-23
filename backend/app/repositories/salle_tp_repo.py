"""SalleTP Repository."""
from sqlmodel import Session, select
from app.models.salle_tp import SalleTP
from app.repositories.base import BaseRepository


class SalleTPRepository(BaseRepository[SalleTP]):
    """Repository for SalleTP (TP Room) entity."""
    
    async def get_by_name(self, session: Session, name: str) -> SalleTP | None:
        """Get room by name."""
        query = select(SalleTP).where(SalleTP.nom_salle == name)
        result = await session.execute(query)
        return result.scalars().first()
    
    async def get_active_rooms(self, session: Session) -> list[SalleTP]:
        """Get all active rooms."""
        query = select(SalleTP).where(SalleTP.is_active == True)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_capacity(self, session: Session, min_capacity: int) -> list[SalleTP]:
        """Get rooms with minimum capacity."""
        query = select(SalleTP).where(
            (SalleTP.capacite >= min_capacity) & (SalleTP.is_active == True)
        )
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_with_internet(self, session: Session) -> list[SalleTP]:
        """Get rooms with internet access."""
        query = select(SalleTP).where(
            (SalleTP.access_internet == True) & (SalleTP.is_active == True)
        )
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_with_projector(self, session: Session) -> list[SalleTP]:
        """Get rooms with projector."""
        query = select(SalleTP).where(
            (SalleTP.videoprojecteur == True) & (SalleTP.is_active == True)
        )
        result = await session.execute(query)
        return result.scalars().all()
