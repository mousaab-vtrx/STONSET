"""Module Repository."""
from sqlmodel import Session, select
from app.models.module import Module
from app.repositories.base import BaseRepository


class ModuleRepository(BaseRepository[Module]):
    """Repository for Module (Course) entity."""
    
    async def get_by_filiere(self, session: Session, filiere_id: int) -> list[Module]:
        """Get all modules in a program."""
        query = select(Module).where(Module.filiere_id == filiere_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_code(self, session: Session, code: str) -> Module | None:
        """Get module by code."""
        query = select(Module).where(Module.code_module == code)
        result = await session.execute(query)
        return result.scalars().first()
    
    async def get_by_name(self, session: Session, name: str) -> list[Module]:
        """Get modules by name (may have duplicates across programs)."""
        query = select(Module).where(Module.nom_module == name)
        result = await session.execute(query)
        return result.scalars().all()
