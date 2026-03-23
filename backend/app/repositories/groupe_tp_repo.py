"""GroupeTP Repository."""
from sqlmodel import Session, select
from app.models.groupe_tp import GroupeTP
from app.repositories.base import BaseRepository


class GroupeTPRepository(BaseRepository[GroupeTP]):
    """Repository for GroupeTP (TP Group) entity."""
    
    async def get_all(
        self, session: Session, skip: int = 0, limit: int = 100, type_filter: str = None
    ) -> list[GroupeTP]:
        """Get all TP groups with optional filtering by session type.
        
        Args:
            session: Database session
            skip: Number of records to skip
            limit: Number of records to return
            type_filter: Optional session type to filter by (CM, TD, TP, EXAM, SEMINAR)
        
        Returns:
            List of GroupeTP objects matching the criteria
        """
        query = select(GroupeTP)
        
        if type_filter:
            query = query.where(GroupeTP.type == type_filter.upper())
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_module(self, session: Session, module_id: int) -> list[GroupeTP]:
        """Get all TP groups in a module."""
        query = select(GroupeTP).where(GroupeTP.module_id == module_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_section(self, session: Session, section_id: int) -> list[GroupeTP]:
        """Get all TP groups in a section."""
        query = select(GroupeTP).where(GroupeTP.section_id == section_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_module_and_number(
        self, session: Session, module_id: int, num_groupe: int
    ) -> GroupeTP | None:
        """Get specific TP group by module and number."""
        query = select(GroupeTP).where(
            (GroupeTP.module_id == module_id) & (GroupeTP.num_groupe == num_groupe)
        )
        result = await session.execute(query)
        return result.scalars().first()
