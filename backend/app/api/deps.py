"""
Dependency injection - FastAPI dependencies.
"""
from typing import AsyncGenerator, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.core.security import verify_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with async_session() as session:
        yield session


async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Get user repository."""
    return UserRepository(db)


async def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo)
) -> UserService:
    """Get user service."""
    return UserService(user_repo)


async def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repo)
) -> AuthService:
    """Get auth service."""
    return AuthService(user_repo)


# JWT Authentication
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Get current authenticated user from JWT token.
    Validates token and returns User object.
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload or "sub" not in payload:
        raise UnauthorizedException("Invalid authentication credentials")
    
    user_id = int(payload["sub"])
    
    # Get user from database
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(db, user_id)
    
    if not user or not user.is_active:
        raise UnauthorizedException("User not found or inactive")
    
    return user


# Role-based Authorization
def has_role(user: User, *required_roles: str) -> bool:
    """
    Check if user has required role, considering hierarchy.
    
    Role hierarchy:
    - responsable_service: Can access all features
    - chef_dept: Inherits enseignant capabilities + department management
    - enseignant: Basic teacher capabilities
    """
    role_hierarchy = {
        "responsable_service": ["responsable_service"],
        "chef_dept": ["chef_dept", "enseignant"],
        "enseignant": ["enseignant"],
    }
    
    user_roles = role_hierarchy.get(user.user_type, [])
    return any(role in user_roles for role in required_roles)


def require_role(*allowed_roles: str) -> Callable:
    """
    Dependency factory for role-based authorization.
    
    Usage:
        @router.get("/admin")
        async def admin_endpoint(
            current_user: User = Depends(require_role("responsable_service"))
        ):
            ...
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_role(current_user, *allowed_roles):
            raise ForbiddenException(
                f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        return current_user
    
    return role_checker
