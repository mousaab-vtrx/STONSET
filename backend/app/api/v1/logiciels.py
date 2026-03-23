"""Logiciel (Software) API Router."""
from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.logiciel import LogicielCreate, LogicielUpdate, LogicielResponse
from app.services.logiciel_service import LogicielService
from app.repositories.logiciel_repo import LogicielRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/logiciels", tags=["logiciels"])


async def get_logiciel_service(db: AsyncSession = Depends(get_db)) -> LogicielService:
    """Dependency to get logiciel service."""
    from app.models.logiciel import Logiciel
    repo = LogicielRepository(db, Logiciel)
    return LogicielService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_logiciel(
    obj_in: LogicielCreate,
    service: LogicielService = Depends(get_logiciel_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new software."""
    try:
        logiciel = await service.create_logiciel(db, obj_in)
        return success_response(data=LogicielResponse.from_orm(logiciel).dict(), message="Logiciel created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{logiciel_id}", response_model=dict)
async def get_logiciel(
    logiciel_id: int,
    service: LogicielService = Depends(get_logiciel_service),
    db: AsyncSession = Depends(get_db)
):
    """Get software by ID."""
    try:
        logiciel = await service.get_logiciel(db, logiciel_id)
        return success_response(data=LogicielResponse.from_orm(logiciel).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/systeme/{systeme_id}", response_model=dict)
async def get_logiciels_by_systeme(
    systeme_id: int,
    service: LogicielService = Depends(get_logiciel_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all software for an OS."""
    try:
        logiciels = await service.get_logiciels_by_systeme(db, systeme_id)
        return success_response(data=[LogicielResponse.from_orm(l).dict() for l in logiciels])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_logiciels(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: LogicielService = Depends(get_logiciel_service),
    db: AsyncSession = Depends(get_db)
):
    """List all software."""
    try:
        logiciels = await service.get_all_logiciels(db, skip=skip, limit=limit)
        return success_response(
            data=[LogicielResponse.from_orm(l).dict() for l in logiciels],
            meta={"skip": skip, "limit": limit}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{logiciel_id}", response_model=dict)
async def update_logiciel(
    logiciel_id: int,
    obj_in: LogicielUpdate,
    service: LogicielService = Depends(get_logiciel_service),
    db: AsyncSession = Depends(get_db)
):
    """Update software."""
    try:
        logiciel = await service.update_logiciel(db, logiciel_id, obj_in)
        return success_response(data=LogicielResponse.from_orm(logiciel).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{logiciel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_logiciel(
    logiciel_id: int,
    current_user: User = Depends(require_role("responsable_service")),
    service: LogicielService = Depends(get_logiciel_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete software. Only responsable_service can delete software."""
    try:
        await service.delete_logiciel(db, logiciel_id)
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )
