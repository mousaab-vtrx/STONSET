"""Module Service."""
from sqlmodel import Session
from app.models.module import Module
from app.schemas.module import ModuleCreate, ModuleUpdate
from app.repositories.module_repo import ModuleRepository
from app.core.exceptions import NotFoundError, ConflictError


class ModuleService:
    """Service for course/module operations."""
    
    def __init__(self, repo: ModuleRepository):
        self.repo = repo
    
    async def create_module(self, session: Session, obj_in: ModuleCreate) -> Module:
        """Create a new course/module."""
        existing = await self.repo.get_by_code(session, obj_in.code_module)
        if existing:
            raise ConflictError(f"Module with code '{obj_in.code_module}' already exists")
        
        db_obj = Module.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_module(self, session: Session, module_id: int) -> Module:
        """Get module by ID."""
        db_obj = await self.repo.get_by_id(session, module_id)
        if not db_obj:
            raise NotFoundError(f"Module with ID {module_id} not found")
        return db_obj
    
    async def get_modules_by_filiere(self, session: Session, filiere_id: int) -> list[Module]:
        """Get all modules in a program."""
        return await self.repo.get_by_filiere(session, filiere_id)
    
    async def get_module_by_code(self, session: Session, code: str) -> Module:
        """Get module by code."""
        db_obj = await self.repo.get_by_code(session, code)
        if not db_obj:
            raise NotFoundError(f"Module with code '{code}' not found")
        return db_obj
    
    async def get_all_modules(self, session: Session, skip: int = 0, limit: int = 10) -> list[Module]:
        """Get all modules."""
        return await self.repo.get_all(session, skip=skip, limit=limit)
    
    async def update_module(
        self, session: Session, module_id: int, obj_in: ModuleUpdate
    ) -> Module:
        """Update module."""
        db_obj = await self.get_module(session, module_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        if "code_module" in update_data:
            existing = await self.repo.get_by_code(session, update_data["code_module"])
            if existing and existing.id != module_id:
                raise ConflictError(f"Module with code '{update_data['code_module']}' already exists")
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_module(self, session: Session, module_id: int) -> None:
        """Delete module."""
        db_obj = await self.get_module(session, module_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
