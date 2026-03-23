"""
Authentication router - POST /api/v1/auth/*.
Handles user registration and login.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_auth_service, get_db
from app.core.exceptions import ApplicationError
from app.schemas.user import UserCreate, UserLoginRequest, UserResponse, RefreshTokenRequest
from app.services.auth_service import AuthService
from app.utils.responses import error_response, success_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Register new user.
    - **email**: User email (unique)
    - **nom_user**: User name
    - **prenom_user**: User first name
    - **password**: Password (min 8 chars)
    - **user_type**: enseignant | chef_dept | responsable_service
    """
    try:
        user = await auth_service.register(user_data)
        await auth_service.commit()
        
        return success_response(
            data=UserResponse.from_orm(user).dict(),
            message="User registered successfully",
            meta={"created": True},
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.post(
    "/login",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="User Login",
)
async def login(
    credentials: UserLoginRequest,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Authenticate user and get access token.
    - **email**: User email
    - **password**: User password
    """
    try:
        user, access_token, refresh_token = await auth_service.login(credentials)

        return success_response(
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": UserResponse.from_orm(user).dict(),
            },
            message="Login successful",
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.post(
    "/refresh-token",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
)
async def refresh_token(
    payload: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Refresh access token using a valid refresh token.
    """
    try:
        user, access_token, refresh_token = await auth_service.refresh_tokens(payload.refresh_token)

        return success_response(
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": UserResponse.from_orm(user).dict(),
            },
            message="Token refreshed successfully",
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.post(
    "/logout",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="User logout",
)
async def logout() -> dict:
    """
    Stateless logout endpoint.

    The client should clear stored tokens; this endpoint exists for
    auditability and future token revocation support.
    """
    return success_response(message="Logout successful")


# TODO: Add more auth endpoints from diagrams
# - POST /refresh-token: Token refresh
# - POST /logout: Token revocation
# - POST /forgot-password: Password reset request
# - POST /verify-email: Email verification
# - POST /change-password: Change password

# async def refresh_token(...): ...
#
# @router.post("/logout")
# async def logout(...): ...
#
# @router.post("/forgot-password")
# async def forgot_password(...): ...
#
# @router.post("/reset-password")
# async def reset_password(...): ...
