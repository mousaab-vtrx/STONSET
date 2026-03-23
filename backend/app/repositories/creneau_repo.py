"""Créneau Repository."""
from sqlmodel import Session, select
from datetime import time
from app.models.creneau import Creneau
from app.repositories.base import BaseRepository


class CreneauRepository(BaseRepository[Creneau]):
    """Repository for Créneau (Time Slot) entity."""
    
    async def get_by_day_and_week(
        self, session: Session, num_jour: int, num_semaine: int
    ) -> list[Creneau]:
        """Get time slots for specific day and week."""
        query = select(Creneau).where(
            (Creneau.num_jour == num_jour) & (Creneau.num_semaine == num_semaine)
        )
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_day(self, session: Session, num_jour: int) -> list[Creneau]:
        """Get all time slots for a day."""
        query = select(Creneau).where(Creneau.num_jour == num_jour)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_time(self, session: Session, heure_debut: time) -> list[Creneau]:
        """Get time slots starting at specific time."""
        query = select(Creneau).where(Creneau.heure_debut == heure_debut)
        result = await session.execute(query)
        return result.scalars().all()
