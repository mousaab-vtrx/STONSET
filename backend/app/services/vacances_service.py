"""Vacances Service."""
from datetime import date
from sqlmodel import Session
from app.models.vacances import Vacances
from app.schemas.vacances import VacancesCreate, VacancesUpdate
from app.repositories.vacances_repo import VacancesRepository
from app.core.exceptions import NotFoundError, ConflictError


class VacancesService:
    """Service for vacation period operations."""
    
    def __init__(self, repo: VacancesRepository):
        self.repo = repo
    
    async def create_vacances(self, session: Session, obj_in: VacancesCreate) -> Vacances:
        """Create a new vacation period."""
        existing = await self.repo.get_by_name(session, obj_in.nom_vacances)
        if existing:
            raise ConflictError(f"Vacation '{obj_in.nom_vacances}' already exists")
        
        db_obj = Vacances.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_vacances(self, session: Session, vacances_id: int) -> Vacances:
        """Get vacation period by ID."""
        db_obj = await self.repo.get_by_id(session, vacances_id)
        if not db_obj:
            raise NotFoundError(f"Vacances with ID {vacances_id} not found")
        return db_obj
    
    async def get_active_vacations(self, session: Session, current_date: date) -> list[Vacances]:
        """Get currently active vacation periods."""
        return await self.repo.get_active_vacations(session, current_date)
    
    async def get_upcoming_vacations(self, session: Session, from_date: date) -> list[Vacances]:
        """Get upcoming vacation periods."""
        return await self.repo.get_upcoming_vacations(session, from_date)
    
    async def get_all_vacances(self, session: Session, skip: int = 0, limit: int = 10) -> list[Vacances]:
        """Get all vacation periods."""
        return await self.repo.get_all(session, skip=skip, limit=limit)
    
    async def update_vacances(
        self, session: Session, vacances_id: int, obj_in: VacancesUpdate
    ) -> Vacances:
        """Update vacation period."""
        db_obj = await self.get_vacances(session, vacances_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_vacances(self, session: Session, vacances_id: int) -> None:
        """Delete vacation period."""
        db_obj = await self.get_vacances(session, vacances_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
