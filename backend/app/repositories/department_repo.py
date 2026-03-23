"""Department Repository."""
from sqlmodel import Session, select
from app.models.department import Department
from app.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    """Repository for Department entity."""
    
    async def get_by_name(self, session: Session, name: str) -> Department | None:
        """Get department by name."""
        query = select(Department).where(Department.nom_department == name)
        result = await session.execute(query)
        return result.scalars().first()
    
    async def get_with_head(self, session: Session) -> list[Department]:
        """Get departments with their heads assigned."""
        query = select(Department).where(Department.chef_department_id.is_not(None))
        result = await session.execute(query)
        return result.scalars().all()
