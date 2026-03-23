"""SalleTP Service."""
from sqlmodel import Session
from app.models.salle_tp import SalleTP
from app.schemas.salle_tp import SalleTPCreate, SalleTPUpdate
from app.repositories.salle_tp_repo import SalleTPRepository
from app.core.exceptions import NotFoundError, ConflictError


class SalleTPService:
    """Service for TP room operations."""
    
    def __init__(self, repo: SalleTPRepository):
        self.repo = repo
    
    async def create_salle_tp(self, session: Session, obj_in: SalleTPCreate) -> SalleTP:
        """Create a new TP room."""
        existing = await self.repo.get_by_name(session, obj_in.nom_salle)
        if existing:
            raise ConflictError(f"Room '{obj_in.nom_salle}' already exists")
        
        db_obj = SalleTP.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_salle_tp(self, session: Session, salle_id: int) -> SalleTP:
        """Get TP room by ID."""
        db_obj = await self.repo.get_by_id(session, salle_id)
        if not db_obj:
            raise NotFoundError(f"SalleTP with ID {salle_id} not found")
        return db_obj
    
    async def get_active_rooms(self, session: Session) -> list[SalleTP]:
        """Get all active rooms."""
        return await self.repo.get_active_rooms(session)
    
    async def get_rooms_by_capacity(self, session: Session, min_capacity: int) -> list[SalleTP]:
        """Get rooms with minimum capacity."""
        return await self.repo.get_by_capacity(session, min_capacity)
    
    async def get_rooms_with_internet(self, session: Session) -> list[SalleTP]:
        """Get rooms with internet access."""
        return await self.repo.get_with_internet(session)
    
    async def get_rooms_with_projector(self, session: Session) -> list[SalleTP]:
        """Get rooms with projector."""
        return await self.repo.get_with_projector(session)
    
    async def get_all_salles_tp(self, session: Session, skip: int = 0, limit: int = 10) -> list[SalleTP]:
        """Get all TP rooms."""
        return await self.repo.get_all(session, skip=skip, limit=limit)
    
    async def update_salle_tp(
        self, session: Session, salle_id: int, obj_in: SalleTPUpdate
    ) -> SalleTP:
        """Update TP room."""
        db_obj = await self.get_salle_tp(session, salle_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_salle_tp(self, session: Session, salle_id: int) -> None:
        """Delete TP room."""
        db_obj = await self.get_salle_tp(session, salle_id)
        # Soft delete by marking inactive
        db_obj.is_active = False
        session.add(db_obj)
        await session.commit()
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
