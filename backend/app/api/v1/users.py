"""
User router - GET/POST/PUT/PATCH/DELETE /api/v1/users/*.
Handles user CRUD operations and profile management.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_user_service
from app.core.exceptions import ApplicationError, NotFoundError, AuthenticationError
from app.core.security import verify_token
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.utils.responses import error_response, success_response

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="List All Users",
)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    """
    Get all users with pagination.
    - **skip**: Number of records to skip
    - **limit**: Number of records to return (max 100)
    """
    try:
        users = await user_service.get_all_users(skip=skip, limit=limit)
        user_responses = [UserResponse.from_orm(u).dict() for u in users]
        
        return success_response(
            data=user_responses,
            message=f"Retrieved {len(user_responses)} users",
            meta={"total": len(user_responses), "skip": skip, "limit": limit},
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get(
    "/active",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="List Active Users",
)
async def list_active_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    """Get all active users with pagination."""
    try:
        users = await user_service.get_active_users(skip=skip, limit=limit)
        user_responses = [UserResponse.from_orm(u).dict() for u in users]
        
        return success_response(
            data=user_responses,
            message=f"Retrieved {len(user_responses)} active users",
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get(
    "/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get User by ID",
)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    """Get user by ID."""
    try:
        user = await user_service.get_user(user_id)
        return success_response(
            data=UserResponse.from_orm(user).dict(),
            message="User retrieved successfully",
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put(
    "/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Update User",
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    """
    Update user by ID.
    - **user_id**: User ID
    - **user_data**: Fields to update
    """
    try:
        user = await user_service.update_user(user_id, user_data)
        await user_service.commit()
        
        return success_response(
            data=UserResponse.from_orm(user).dict(),
            message="User updated successfully",
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.patch(
    "/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Partially Update User",
)
async def patch_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    """
    Partially update user (same as PUT for this simple app).
    """
    return await update_user(user_id, user_data, user_service)


@router.delete(
    "/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Delete User",
)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    """Delete user by ID (soft delete)."""
    try:
        await user_service.delete_user(user_id)
        await user_service.commit()
        
        return success_response(
            data=None,
            message="User deleted successfully",
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.post(
    "/generate-management-code",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Generate Management Code",
)
async def generate_management_code(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
) -> dict:
    """Generate unique management code for a manager (Chef de Département or Responsable du Service)."""
    try:
        # Extract token from Authorization header
        if not authorization or not authorization.startswith("Bearer "):
            raise AuthenticationError("Missing or invalid authorization header")
        
        token = authorization.replace("Bearer ", "")
        token_data = verify_token(token)
        
        if not token_data or "sub" not in token_data:
            raise AuthenticationError("Invalid token")
        
        current_user_id = int(token_data["sub"])
        
        code = await user_service.generate_management_code(current_user_id)
        await user_service.commit()
        
        return success_response(
            data={"management_code": code},
            message="Management code generated successfully",
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.post(
    "/regenerate-management-code",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Regenerate Management Code",
)
async def regenerate_management_code(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
) -> dict:
    """Regenerate management code (invalidates old code)."""
    try:
        # Extract token from Authorization header
        if not authorization or not authorization.startswith("Bearer "):
            raise AuthenticationError("Missing or invalid authorization header")
        
        token = authorization.replace("Bearer ", "")
        token_data = verify_token(token)
        
        if not token_data or "sub" not in token_data:
            raise AuthenticationError("Invalid token")
        
        current_user_id = int(token_data["sub"])
        
        code = await user_service.regenerate_management_code(current_user_id)
        await user_service.commit()
        
        return success_response(
            data={"management_code": code},
            message="Management code regenerated successfully",
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


# TODO: Add authenticated endpoints for user profile management
# From diagrams use cases:
#
# ENSEIGNANT (Figure 1):
# @router.get("/me")
# async def get_current_enseignant(current_user: User = Depends(get_current_user)): ...
#
# @router.put("/me")
# async def update_enseignant_profile(user_data: UserUpdate, ...): ...
#
# @router.get("/me/reservations")
# async def get_enseignant_reservations(current_user: User = ...): ...
#
# CHEF DE DÉPARTEMENT (Figure 2):
# @router.get("/department/{dept_id}/teachers")
# async def get_department_teachers(dept_id: int, ...): ...
#
# @router.post("/department/{dept_id}/teachers")
# async def add_teacher_to_department(dept_id: int, user_id: int, ...): ...
#
# @router.delete("/department/{dept_id}/teachers/{user_id}")
# async def remove_teacher_from_department(dept_id: int, user_id: int, ...): ...
#
# RESPONSABLE DU SERVICE (Figure 3):
# @router.get("/me")
# async def get_current_service_manager(current_user: User = ...): ...
#
# @router.put("/me")
# async def update_service_manager_info(user_data: UserUpdate, ...): ...

