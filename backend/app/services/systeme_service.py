"""Système Service."""
from sqlmodel import Session
from app.models.systeme import Systeme
from app.schemas.systeme import SystemeCreate, SystemeUpdate
from app.repositories.systeme_repo import SystemeRepository
from app.core.exceptions import NotFoundError, ConflictError


class SystemeService:
    """Service for operating system operations."""
    
    def __init__(self, repo: SystemeRepository):
        self.repo = repo
    
    async def create_systeme(self, session: Session, obj_in: SystemeCreate) -> Systeme:
        """Create a new operating system."""
        existing = await self.repo.get_by_name(session, obj_in.nom_systeme)
        if existing:
            raise ConflictError(f"System '{obj_in.nom_systeme}' already exists")
        
        db_obj = Systeme.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_systeme(self, session: Session, systeme_id: int) -> Systeme:
        """Get OS by ID."""
        db_obj = await self.repo.get_by_id(session, systeme_id)
        if not db_obj:
            raise NotFoundError(f"Système with ID {systeme_id} not found")
        return db_obj
    
    async def get_all_systemes(self, session: Session) -> list[Systeme]:
        """Get all operating systems."""
        return await self.repo.get_all_systems(session)
    
    async def update_systeme(
        self, session: Session, systeme_id: int, obj_in: SystemeUpdate
    ) -> Systeme:
        """Update operating system."""
        db_obj = await self.get_systeme(session, systeme_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_systeme(self, session: Session, systeme_id: int) -> None:
        """Delete operating system."""
        db_obj = await self.get_systeme(session, systeme_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
