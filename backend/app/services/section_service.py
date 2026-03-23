"""Section Service."""
from sqlmodel import Session
from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate
from app.repositories.section_repo import SectionRepository
from app.core.exceptions import NotFoundError


class SectionService:
    """Service for class section operations."""
    
    def __init__(self, repo: SectionRepository):
        self.repo = repo
    
    async def create_section(self, session: Session, obj_in: SectionCreate) -> Section:
        """Create a new section."""
        db_obj = Section.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_section(self, session: Session, section_id: int) -> Section:
        """Get section by ID."""
        db_obj = await self.repo.get_by_id(session, section_id)
        if not db_obj:
            raise NotFoundError(f"Section with ID {section_id} not found")
        return db_obj
    
    async def get_sections_by_module(self, session: Session, module_id: int) -> list[Section]:
        """Get all sections in a module."""
        return await self.repo.get_by_module(session, module_id)
    
    async def get_all_sections(self, session: Session, skip: int = 0, limit: int = 10) -> list[Section]:
        """Get all sections."""
        return await self.repo.get_all(session, skip=skip, limit=limit)
    
    async def update_section(
        self, session: Session, section_id: int, obj_in: SectionUpdate
    ) -> Section:
        """Update section."""
        db_obj = await self.get_section(session, section_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_section(self, session: Session, section_id: int) -> None:
        """Delete section."""
        db_obj = await self.get_section(session, section_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
