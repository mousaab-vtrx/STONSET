"""Logiciel Service."""
from sqlmodel import Session
from app.models.logiciel import Logiciel
from app.schemas.logiciel import LogicielCreate, LogicielUpdate
from app.repositories.logiciel_repo import LogicielRepository
from app.core.exceptions import NotFoundError


class LogicielService:
    """Service for software operations."""
    
    def __init__(self, repo: LogicielRepository):
        self.repo = repo
    
    async def create_logiciel(self, session: Session, obj_in: LogicielCreate) -> Logiciel:
        """Create a new software."""
        db_obj = Logiciel.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_logiciel(self, session: Session, logiciel_id: int) -> Logiciel:
        """Get software by ID."""
        db_obj = await self.repo.get_by_id(session, logiciel_id)
        if not db_obj:
            raise NotFoundError(f"Logiciel with ID {logiciel_id} not found")
        return db_obj
    
    async def get_logiciels_by_systeme(self, session: Session, systeme_id: int) -> list[Logiciel]:
        """Get all software for an OS."""
        return await self.repo.get_by_systeme(session, systeme_id)
    
    async def get_all_logiciels(self, session: Session, skip: int = 0, limit: int = 10) -> list[Logiciel]:
        """Get all software."""
        return await self.repo.get_all(session, skip=skip, limit=limit)
    
    async def update_logiciel(
        self, session: Session, logiciel_id: int, obj_in: LogicielUpdate
    ) -> Logiciel:
        """Update software."""
        db_obj = await self.get_logiciel(session, logiciel_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_logiciel(self, session: Session, logiciel_id: int) -> None:
        """Delete software."""
        db_obj = await self.get_logiciel(session, logiciel_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
