"""Department Service."""
from sqlmodel import Session
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.repositories.department_repo import DepartmentRepository
from app.core.exceptions import NotFoundError, ConflictError


class DepartmentService:
    """Service for department operations."""
    
    def __init__(self, repo: DepartmentRepository):
        self.repo = repo
    
    async def create_department(self, session: Session, obj_in: DepartmentCreate) -> Department:
        """Create a new department."""
        existing = await self.repo.get_by_name(session, obj_in.nom_department)
        if existing:
            raise ConflictError(f"Department '{obj_in.nom_department}' already exists")
        
        db_obj = Department.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_department(self, session: Session, department_id: int) -> Department:
        """Get department by ID."""
        db_obj = await self.repo.get_by_id(session, department_id)
        if not db_obj:
            raise NotFoundError(f"Department with ID {department_id} not found")
        return db_obj
    
    async def get_all_departments(self, session: Session, skip: int = 0, limit: int = 10) -> list[Department]:
        """Get all departments."""
        return await self.repo.get_all(session, skip=skip, limit=limit)
    
    async def update_department(
        self, session: Session, department_id: int, obj_in: DepartmentUpdate
    ) -> Department:
        """Update department."""
        db_obj = await self.get_department(session, department_id)
        update_data = obj_in.dict(exclude_unset=True)
        
        if "nom_department" in update_data:
            existing = await self.repo.get_by_name(session, update_data["nom_department"])
            if existing and existing.id != department_id:
                raise ConflictError(f"Department '{update_data['nom_department']}' already exists")
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_department(self, session: Session, department_id: int) -> None:
        """Delete department."""
        db_obj = await self.get_department(session, department_id)
        await self.repo.delete(session, db_obj)
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
