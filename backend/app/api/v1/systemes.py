"""Système (Operating System) API Router."""
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.systeme import SystemeCreate, SystemeUpdate, SystemeResponse
from app.services.systeme_service import SystemeService
from app.repositories.systeme_repo import SystemeRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/systemes", tags=["systemes"])


async def get_systeme_service(db: AsyncSession = Depends(get_db)) -> SystemeService:
    """Dependency to get systeme service."""
    from app.models.systeme import Systeme
    repo = SystemeRepository(db, Systeme)
    return SystemeService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_systeme(
    obj_in: SystemeCreate,
    service: SystemeService = Depends(get_systeme_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new operating system."""
    try:
        systeme = await service.create_systeme(db, obj_in)
        return success_response(data=SystemeResponse.from_orm(systeme).dict(), message="Système created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{systeme_id}", response_model=dict)
async def get_systeme(
    systeme_id: int,
    service: SystemeService = Depends(get_systeme_service),
    db: AsyncSession = Depends(get_db)
):
    """Get OS by ID."""
    try:
        systeme = await service.get_systeme(db, systeme_id)
        return success_response(data=SystemeResponse.from_orm(systeme).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_systemes(
    service: SystemeService = Depends(get_systeme_service),
    db: AsyncSession = Depends(get_db)
):
    """List all operating systems."""
    try:
        systemes = await service.get_all_systemes(db)
        return success_response(data=[SystemeResponse.from_orm(s).dict() for s in systemes])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{systeme_id}", response_model=dict)
async def update_systeme(
    systeme_id: int,
    obj_in: SystemeUpdate,
    service: SystemeService = Depends(get_systeme_service),
    db: AsyncSession = Depends(get_db)
):
    """Update operating system."""
    try:
        systeme = await service.update_systeme(db, systeme_id, obj_in)
        return success_response(data=SystemeResponse.from_orm(systeme).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{systeme_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_systeme(
    systeme_id: int,
    current_user: User = Depends(require_role("responsable_service")),
    service: SystemeService = Depends(get_systeme_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete operating system. Only responsable_service can delete systems."""
    try:
        await service.delete_systeme(db, systeme_id)
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )
