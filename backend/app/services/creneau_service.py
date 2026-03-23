"""Créneau Service."""
from sqlmodel import Session
from app.models.creneau import Creneau
from app.schemas.creneau import CreneauCreate, CreneauUpdate
from app.repositories.creneau_repo import CreneauRepository
from app.core.exceptions import NotFoundError


class CreneauService:
    """Service for time slot operations."""
    
    def __init__(self, repo: CreneauRepository):
        self.repo = repo
    
    async def create_creneau(self, session: Session, obj_in: CreneauCreate) -> Creneau:
        """Create a new time slot."""
        db_obj = Creneau.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_creneau(self, session: Session, creneau_id: int) -> Creneau:
        """Get time slot by ID."""
        db_obj = await self.repo.get_by_id(session, creneau_id)
        if not db_obj:
            raise NotFoundError(f"Créneau with ID {creneau_id} not found")
        return db_obj
    
    async def get_creneaux_by_day_week(
        self, session: Session, num_jour: int, num_semaine: int
    ) -> list[Creneau]:
        """Get time slots for specific day and week."""
        return await self.repo.get_by_day_and_week(session, num_jour, num_semaine)
    
    async def get_creneaux_by_day(self, session: Session, num_jour: int) -> list[Creneau]:
        """Get all time slots for a day."""
        return await self.repo.get_by_day(session, num_jour)
    
    async def get_all_creneaux(self, session: Session, skip: int = 0, limit: int = 10) -> list[Creneau]:
        """Get all time slots."""
        return await self.repo.get_all(session, skip=skip, limit=limit)
    
    async def update_creneau(
        self, session: Session, creneau_id: int, obj_in: CreneauUpdate
    ) -> Creneau:
        """Update time slot."""
        db_obj = await self.get_creneau(session, creneau_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_creneau(self, session: Session, creneau_id: int) -> None:
        """Delete time slot."""
        db_obj = await self.get_creneau(session, creneau_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
