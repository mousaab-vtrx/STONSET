"""
User service - Business logic for user operations.
Framework-agnostic, completely independent from FastAPI.
Handles user CRUD operations and user-specific business logic.
"""
from typing import Optional
import secrets

from app.core.exceptions import ConflictError, NotFoundError, AuthenticationError
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    """User service."""

    def __init__(self, user_repo: UserRepository):
        """Initialize user service."""
        self.user_repo = user_repo

    async def get_user(self, user_id: int) -> User:
        """Get user by ID."""
        user = await self.user_repo.get_by_id(self.user_repo.session, user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all users with pagination."""
        return await self.user_repo.get_all(skip=skip, limit=limit)

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all active users with pagination."""
        return await self.user_repo.get_active_users(skip=skip, limit=limit)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update user."""
        user = await self.user_repo.get_by_id(self.user_repo.session, user_id)
        if not user:
            raise NotFoundError("User not found")

        # Check if new email is already taken
        if user_data.email and user_data.email != user.email:
            existing = await self.user_repo.get_by_email(user_data.email)
            if existing:
                raise ConflictError("Email already in use")

        updated_user = await self.user_repo.update(user_id, user_data)
        return updated_user

    async def delete_user(self, user_id: int) -> bool:
        """Delete user (soft delete via is_active)."""
        user = await self.user_repo.get_by_id(self.user_repo.session, user_id)
        if not user:
            raise NotFoundError("User not found")

        # Soft delete
        user.is_active = False
        self.user_repo.session.add(user)
        await self.user_repo.session.flush()
        return True

    async def commit(self) -> None:
        """Commit changes."""
        await self.user_repo.commit()

    async def generate_management_code(self, user_id: int) -> str:
        """Generate unique management code for a manager."""
        user = await self.user_repo.get_by_id(self.user_repo.session, user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Check if user has authority to generate code
        if user.user_type not in ["chef_dept", "responsable_service"]:
            raise AuthenticationError("Only department heads and service managers can generate management codes")
        
        # Generate unique 8-character alphanumeric code
        while True:
            code = secrets.token_urlsafe(6)[:8].upper()
            existing = await self.user_repo.get_by_management_code(code)
            if not existing:
                break
        
        user.management_code = code
        self.user_repo.session.add(user)
        await self.user_repo.session.flush()
        return code

    async def regenerate_management_code(self, user_id: int) -> str:
        """Regenerate management code for a manager."""
        user = await self.user_repo.get_by_id(self.user_repo.session, user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Check if user has authority
        if user.user_type not in ["chef_dept", "responsable_service"]:
            raise AuthenticationError("Only department heads and service managers can regenerate management codes")
        
        # Generate new unique code
        while True:
            code = secrets.token_urlsafe(6)[:8].upper()
            existing = await self.user_repo.get_by_management_code(code)
            if not existing:
                break
        
        user.management_code = code
        self.user_repo.session.add(user)
        await self.user_repo.session.flush()
        return code

    # TODO: Add more user logic from diagrams
    # From Figure 1 (Enseignant use cases):
    # - get_teacher_reservations(user_id) -> List[Reservation]
    # - update_teacher_info(user_id, info) -> User
    # 
    # From Figure 2 (Chef de département use cases):
    # - get_department_teachers(dept_id) -> List[User]
    # - add_teacher_to_department(user_id, dept_id) -> User
    # - remove_teacher_from_department(user_id) -> bool
    #
    # From Figure 3 (Responsable du service use cases):
    # - update_service_manager_info(user_id, info) -> User

