"""
Authentication service - Business logic for auth operations.
Framework-agnostic, completely independent from FastAPI.
Handles user registration, login, and token validation.
"""
from datetime import timedelta
from typing import Optional

from app.core.exceptions import AuthenticationError, ConflictError
from app.core.security import create_access_token, get_password_hash, verify_password, verify_token
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserLoginRequest


class AuthService:
    """Authentication service."""

    def __init__(self, user_repo: UserRepository):
        """Initialize auth service."""
        self.user_repo = user_repo

    async def register(self, user_data: UserCreate) -> User:
        """Register new user."""
        # Check if user already exists
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ConflictError(
                "This email is already registered. Try signing in or use another email.",
            )

        # Hash password
        hashed_password = get_password_hash(user_data.password)

        # If user provides a management code, find the supervisor
        supervisor_id = None
        if user_data.management_code:
            supervisor = await self.user_repo.get_by_management_code(user_data.management_code)
            if not supervisor:
                raise AuthenticationError(
                    "That invite code didn't work. Please check it with your manager.",
                    status_code=400,
                    code="INVALID_MANAGEMENT_CODE",
                )
            supervisor_id = supervisor.id

        # Create user
        db_user = User(
            email=user_data.email,
            nom_user=user_data.nom_user,
            prenom_user=user_data.prenom_user,
            hashed_password=hashed_password,
            is_active=True,
            user_type=user_data.user_type,
            supervisor_id=supervisor_id,
        )
        self.user_repo.session.add(db_user)
        await self.user_repo.session.flush()
        await self.user_repo.session.refresh(db_user)
        
        return db_user

    async def login(self, credentials: UserLoginRequest) -> tuple[User, str, str]:
        """Authenticate user and return (user, access_token, refresh_token)."""
        user = await self.user_repo.get_by_email(credentials.email)
        
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise AuthenticationError(
                "We couldn't sign you in. Please check your email and password.",
                status_code=401,
                code="INVALID_CREDENTIALS",
            )

        if not user.is_active:
            raise AuthenticationError(
                "Your account is inactive. Please contact support.",
                status_code=403,
                code="ACCOUNT_INACTIVE",
            )

        # Create access token
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "user_type": user.user_type,
            },
            expires_delta=timedelta(minutes=30)
        )

        # Create refresh token (longer-lived, marked as refresh)
        refresh_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "user_type": user.user_type,
                "token_type": "refresh",
            },
            expires_delta=timedelta(days=7),
        )

        return user, access_token, refresh_token

    async def get_user_from_token(self, user_id: int) -> Optional[User]:
        """Get user by ID (from token)."""
        return await self.user_repo.get_by_id(user_id)

    async def refresh_tokens(self, refresh_token: str) -> tuple[User, str, str]:
        """Validate refresh token and issue new access/refresh token pair."""
        payload = verify_token(refresh_token)

        if not payload or payload.get("token_type") != "refresh" or "sub" not in payload:
            raise AuthenticationError(
                "Your session has expired. Please sign in again.",
                status_code=401,
                code="INVALID_REFRESH_TOKEN",
            )

        user_id = int(payload["sub"])
        user = await self.user_repo.get_by_id(user_id)

        if not user or not user.is_active:
            raise AuthenticationError(
                "Your account is inactive. Please contact support.",
                status_code=403,
                code="ACCOUNT_INACTIVE",
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "user_type": user.user_type,
            },
            expires_delta=timedelta(minutes=30),
        )

        # Rotate refresh token
        new_refresh_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "user_type": user.user_type,
                "token_type": "refresh",
            },
            expires_delta=timedelta(days=7),
        )

        return user, access_token, new_refresh_token

    async def commit(self) -> None:
        """Commit changes."""
        await self.user_repo.commit()

    # TODO: Add more auth logic from diagrams
    # - Password reset functionality
    # - Email verification
    # - Token refresh
    # - Multi-factor authentication
    # From use cases: Figure 1, Figure 2, Figure 3

