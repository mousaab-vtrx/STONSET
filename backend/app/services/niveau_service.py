"""Niveau Service."""
from sqlmodel import Session
from app.models.niveau import Niveau
from app.schemas.niveau import NiveauCreate, NiveauUpdate
from app.repositories.niveau_repo import NiveauRepository
from app.core.exceptions import NotFoundError, ConflictError


class NiveauService:
    """Service for academic level operations."""
    
    def __init__(self, repo: NiveauRepository):
        self.repo = repo
    
    async def create_niveau(self, session: Session, obj_in: NiveauCreate) -> Niveau:
        """Create a new academic level."""
        existing = await self.repo.get_by_name(session, obj_in.nom_niveau)
        if existing:
            raise ConflictError(f"Niveau '{obj_in.nom_niveau}' already exists")
        
        db_obj = Niveau.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_niveau(self, session: Session, niveau_id: int) -> Niveau:
        """Get academic level by ID."""
        db_obj = await self.repo.get_by_id(session, niveau_id)
        if not db_obj:
            raise NotFoundError(f"Niveau with ID {niveau_id} not found")
        return db_obj
    
    async def get_niveaux_by_department(self, session: Session, department_id: int) -> list[Niveau]:
        """Get all levels in a department."""
        return await self.repo.get_by_department(session, department_id)
    
    async def get_all_niveaux(self, session: Session, skip: int = 0, limit: int = 10) -> list[Niveau]:
        """Get all academic levels."""
        return await self.repo.get_all(session, skip=skip, limit=limit)
    
    async def update_niveau(
        self, session: Session, niveau_id: int, obj_in: NiveauUpdate
    ) -> Niveau:
        """Update academic level."""
        db_obj = await self.get_niveau(session, niveau_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_niveau(self, session: Session, niveau_id: int) -> None:
        """Delete academic level."""
        db_obj = await self.get_niveau(session, niveau_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
