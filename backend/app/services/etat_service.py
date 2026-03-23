"""Etat Service."""
from sqlmodel import Session
from app.models.etat import Etat
from app.schemas.etat import EtatCreate, EtatUpdate
from app.repositories.etat_repo import EtatRepository
from app.core.exceptions import NotFoundError, ConflictError


class EtatService:
    """Service for status operations."""
    
    def __init__(self, repo: EtatRepository):
        self.repo = repo
    
    async def create_etat(self, session: Session, obj_in: EtatCreate) -> Etat:
        """Create a new status."""
        existing = await self.repo.get_by_name(session, obj_in.nom_etat)
        if existing:
            raise ConflictError(f"Status '{obj_in.nom_etat}' already exists")
        
        db_obj = Etat.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_etat(self, session: Session, etat_id: int) -> Etat:
        """Get status by ID."""
        db_obj = await self.repo.get_by_id(session, etat_id)
        if not db_obj:
            raise NotFoundError(f"Etat with ID {etat_id} not found")
        return db_obj
    
    async def get_etat_by_name(self, session: Session, name: str) -> Etat:
        """Get status by name."""
        db_obj = await self.repo.get_by_name(session, name)
        if not db_obj:
            raise NotFoundError(f"Status '{name}' not found")
        return db_obj
    
    async def get_all_etats(self, session: Session) -> list[Etat]:
        """Get all statuses."""
        return await self.repo.get_all_statuses(session)
    
    async def update_etat(
        self, session: Session, etat_id: int, obj_in: EtatUpdate
    ) -> Etat:
        """Update status."""
        db_obj = await self.get_etat(session, etat_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_etat(self, session: Session, etat_id: int) -> None:
        """Delete status."""
        db_obj = await self.get_etat(session, etat_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
