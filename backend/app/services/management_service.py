"""
Management Service - For managers to manage their subordinates.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.utils.management_code import generate_management_code


class ManagementService:
    """
    Service for managing subordinates (enseignants under chef_dept, etc.)
    
    Hierarchy:
    - responsable_service (manages multiple chef_dept)
    - chef_dept (manages multiple enseignant)
    - enseignant (can be managed by chef_dept)
    """
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def generate_management_code(self, session: AsyncSession, user_id: int) -> str:
        """
        Generate a unique management code for a user.
        
        Args:
            session: Database session
            user_id: The ID of the manager
        
        Returns:
            Generated management code
        """
        user = await self.user_repo.get_by_id(session, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Generate code
        code = generate_management_code(user_id, user.user_type)
        
        # Save to user
        user.management_code = code
        session.add(user)
        await session.flush()
        
        return code
    
    async def get_subordinates(self, session: AsyncSession, manager_id: int) -> List[User]:
        """
        Get all subordinates of a manager.
        
        Args:
            session: Database session
            manager_id: The ID of the manager
        
        Returns:
            List of subordinate users
        """
        statement = select(User).where(User.supervisor_id == manager_id)
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def add_subordinate_by_code(self, session: AsyncSession, manager_id: int, management_code: str) -> User:
        """
        Add a subordinate to a manager using the manager's management code.
        This allows enseignants to register under a chef_dept.
        
        Args:
            session: Database session
            manager_id: The ID of the manager
            management_code: The manager's management code
        
        Returns:
            The user that was promoted/assigned
        """
        # Verify manager exists and has this code
        manager = await self.user_repo.get_by_id(session, manager_id)
        if not manager or manager.management_code != management_code:
            raise ValueError("Invalid management code")
        
        # Check manager is actually a manager
        if manager.user_type not in ['chef_dept', 'responsable_service']:
            raise ValueError("User is not a manager")
        
        return manager
    
    async def remove_subordinate(self, session: AsyncSession, manager_id: int, subordinate_id: int) -> bool:
        """
        Remove a subordinate from a manager.
        
        Args:
            session: Database session
            manager_id: The ID of the manager
            subordinate_id: The ID of the subordinate
        
        Returns:
            True if successful
        """
        # Get subordinate
        subordinate = await self.user_repo.get_by_id(session, subordinate_id)
        if not subordinate or subordinate.supervisor_id != manager_id:
            return False
        
        # Remove supervisor link
        subordinate.supervisor_id = None
        session.add(subordinate)
        await session.flush()
        
        return True
    
    async def list_all_subordinates_recursive(
        self, session: AsyncSession, manager_id: int, max_depth: int = 5
    ) -> List[User]:
        """
        Get all subordinates recursively (subordinates of subordinates).
        
        Args:
            session: Database session
            manager_id: The ID of the manager
            max_depth: Maximum depth to search
        
        Returns:
            List of all subordinates
        """
        all_subordinates = []
        current_level = [manager_id]
        depth = 0
        
        while current_level and depth < max_depth:
            next_level = []
            for manager in current_level:
                subordinates = await self.get_subordinates(session, manager)
                all_subordinates.extend(subordinates)
                next_level.extend([s.id for s in subordinates])
            
            current_level = next_level
            depth += 1
        
        return all_subordinates
