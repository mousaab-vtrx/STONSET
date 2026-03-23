"""GroupeTP Service."""
from sqlmodel import Session
from app.models.groupe_tp import GroupeTP
from app.schemas.groupe_tp import GroupeTPCreate, GroupeTPUpdate
from app.repositories.groupe_tp_repo import GroupeTPRepository
from app.core.exceptions import NotFoundError


class GroupeTPService:
    """Service for TP group operations."""
    
    def __init__(self, repo: GroupeTPRepository):
        self.repo = repo
    
    async def create_groupe_tp(self, session: Session, obj_in: GroupeTPCreate) -> GroupeTP:
        """Create a new TP group."""
        db_obj = GroupeTP.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_groupe_tp(self, session: Session, groupe_id: int) -> GroupeTP:
        """Get TP group by ID."""
        db_obj = await self.repo.get_by_id(session, groupe_id)
        if not db_obj:
            raise NotFoundError(f"GroupeTP with ID {groupe_id} not found")
        return db_obj
    
    async def get_groupes_by_module(self, session: Session, module_id: int) -> list[GroupeTP]:
        """Get all TP groups in a module."""
        return await self.repo.get_by_module(session, module_id)
    
    async def get_groupes_by_section(self, session: Session, section_id: int) -> list[GroupeTP]:
        """Get all TP groups in a section."""
        return await self.repo.get_by_section(session, section_id)
    
    async def get_all_groupes_tp(
        self, session: Session, skip: int = 0, limit: int = 10, type_filter: str = None
    ) -> list[GroupeTP]:
        """Get all TP groups, optionally filtered by session type.
        
        Args:
            session: Database session
            skip: Number of records to skip
            limit: Number of records to return
            type_filter: Optional session type to filter by (CM, TD, TP, EXAM, SEMINAR)
        """
        return await self.repo.get_all(session, skip=skip, limit=limit, type_filter=type_filter)
    
    async def update_groupe_tp(
        self, session: Session, groupe_id: int, obj_in: GroupeTPUpdate
    ) -> GroupeTP:
        """Update TP group."""
        db_obj = await self.get_groupe_tp(session, groupe_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_groupe_tp(self, session: Session, groupe_id: int) -> None:
        """Delete TP group."""
        db_obj = await self.get_groupe_tp(session, groupe_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
