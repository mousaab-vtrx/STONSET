"""Filière Service."""
from sqlmodel import Session
from app.models.filiere import Filiere
from app.schemas.filiere import FiliereCreate, FiliereUpdate
from app.repositories.filiere_repo import FiliereRepository
from app.core.exceptions import NotFoundError, ConflictError


class FiliereService:
    """Service for academic program operations."""
    
    def __init__(self, repo: FiliereRepository):
        self.repo = repo
    
    async def create_filiere(self, session: Session, obj_in: FiliereCreate) -> Filiere:
        """Create a new academic program."""
        existing = await self.repo.get_by_name(session, obj_in.nom_filiere)
        if existing:
            raise ConflictError(f"Filière '{obj_in.nom_filiere}' already exists")
        
        db_obj = Filiere.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_filiere(self, session: Session, filiere_id: int) -> Filiere:
        """Get academic program by ID."""
        db_obj = await self.repo.get_by_id(session, filiere_id)
        if not db_obj:
            raise NotFoundError(f"Filière with ID {filiere_id} not found")
        return db_obj
    
    async def get_filieres_by_niveau(self, session: Session, niveau_id: int) -> list[Filiere]:
        """Get all programs in a level."""
        return await self.repo.get_by_niveau(session, niveau_id)
    
    async def get_all_filieres(self, session: Session, skip: int = 0, limit: int = 10) -> list[Filiere]:
        """Get all academic programs."""
        return await self.repo.get_all(session, skip=skip, limit=limit)
    
    async def update_filiere(
        self, session: Session, filiere_id: int, obj_in: FiliereUpdate
    ) -> Filiere:
        """Update academic program."""
        db_obj = await self.get_filiere(session, filiere_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_filiere(self, session: Session, filiere_id: int) -> None:
        """Delete academic program."""
        db_obj = await self.get_filiere(session, filiere_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
