"""Vacances Repository."""
from sqlmodel import Session, select
from datetime import date
from app.models.vacances import Vacances
from app.repositories.base import BaseRepository


class VacancesRepository(BaseRepository[Vacances]):
    """Repository for Vacances (Vacation) entity."""
    
    async def get_by_name(self, session: Session, name: str) -> Vacances | None:
        """Get vacation by name."""
        query = select(Vacances).where(Vacances.nom_vacances == name)
        result = await session.execute(query)
        return result.scalars().first()
    
    async def get_active_vacations(self, session: Session, current_date: date) -> list[Vacances]:
        """Get vacations that are currently active."""
        query = select(Vacances).where(
            (Vacances.date_debut <= current_date) & (Vacances.date_fin >= current_date)
        )
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_upcoming_vacations(self, session: Session, from_date: date) -> list[Vacances]:
        """Get vacations starting from a date."""
        query = select(Vacances).where(Vacances.date_debut >= from_date).order_by(Vacances.date_debut)
        result = await session.execute(query)
        return result.scalars().all()
