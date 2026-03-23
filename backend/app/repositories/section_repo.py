"""Section Repository."""
from sqlmodel import Session, select
from app.models.section import Section
from app.repositories.base import BaseRepository


class SectionRepository(BaseRepository[Section]):
    """Repository for Section (Class Group) entity."""
    
    async def get_by_module(self, session: Session, module_id: int) -> list[Section]:
        """Get all sections in a module."""
        query = select(Section).where(Section.module_id == module_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_number(self, session: Session, module_id: int, numero: int) -> Section | None:
        """Get section by number within a module."""
        query = select(Section).where(
            (Section.module_id == module_id) & (Section.numero_section == numero)
        )
        result = await session.execute(query)
        return result.scalars().first()
