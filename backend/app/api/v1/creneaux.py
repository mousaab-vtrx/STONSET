"""Créneau (Time Slot) API Router."""
from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user, require_role
from app.models.user import User
from app.schemas.creneau import CreneauCreate, CreneauUpdate, CreneauResponse
from app.services.creneau_service import CreneauService
from app.repositories.creneau_repo import CreneauRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/creneaux", tags=["creneaux"])


async def get_creneau_service(db: AsyncSession = Depends(get_db)) -> CreneauService:
    """Dependency to get creneau service."""
    from app.models.creneau import Creneau
    repo = CreneauRepository(db, Creneau)
    return CreneauService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_creneau(
    obj_in: CreneauCreate,
    current_user: User = Depends(require_role("responsable_service")),
    service: CreneauService = Depends(get_creneau_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new time slot. Only service managers can create time slots."""
    try:
        creneau = await service.create_creneau(db, obj_in)
        return success_response(data=CreneauResponse.from_orm(creneau).dict(), message="Créneau created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{creneau_id}", response_model=dict)
async def get_creneau(
    creneau_id: int,
    current_user: User = Depends(get_current_user),
    service: CreneauService = Depends(get_creneau_service),
    db: AsyncSession = Depends(get_db)
):
    """Get time slot by ID. Requires authentication."""
    try:
        creneau = await service.get_creneau(db, creneau_id)
        return success_response(data=CreneauResponse.from_orm(creneau).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/day/{num_jour}", response_model=dict)
async def get_creneaux_by_day(
    num_jour: int,
    current_user: User = Depends(get_current_user),
    service: CreneauService = Depends(get_creneau_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all time slots for a day. Requires authentication."""
    try:
        creneaux = await service.get_creneaux_by_day(db, num_jour)
        return success_response(data=[CreneauResponse.from_orm(c).dict() for c in creneaux])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/day-week/{num_jour}/{num_semaine}", response_model=dict)
async def get_creneaux_by_day_week(
    num_jour: int,
    num_semaine: int,
    current_user: User = Depends(get_current_user),
    service: CreneauService = Depends(get_creneau_service),
    db: AsyncSession = Depends(get_db)
):
    """Get time slots for specific day and week. Requires authentication."""
    try:
        creneaux = await service.get_creneaux_by_day_week(db, num_jour, num_semaine)
        return success_response(data=[CreneauResponse.from_orm(c).dict() for c in creneaux])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_creneaux(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: CreneauService = Depends(get_creneau_service),
    db: AsyncSession = Depends(get_db)
):
    """List all time slots. Requires authentication."""
    try:
        creneaux = await service.get_all_creneaux(db, skip=skip, limit=limit)
        return success_response(
            data=[CreneauResponse.from_orm(c).dict() for c in creneaux],
            meta={"skip": skip, "limit": limit}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{creneau_id}", response_model=dict)
async def update_creneau(
    creneau_id: int,
    obj_in: CreneauUpdate,
    current_user: User = Depends(require_role("responsable_service")),
    service: CreneauService = Depends(get_creneau_service),
    db: AsyncSession = Depends(get_db)
):
    """Update time slot. Only service managers can update time slots."""
    try:
        creneau = await service.update_creneau(db, creneau_id, obj_in)
        return success_response(data=CreneauResponse.from_orm(creneau).dict())
    except ApplicationError as e:
        return error_response(message=e.message, status_code=e.status_code)


@router.delete("/{creneau_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_creneau(
    creneau_id: int,
    current_user: User = Depends(require_role("responsable_service")),
    service: CreneauService = Depends(get_creneau_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete time slot. Only service managers can delete time slots."""
    try:
        await service.delete_creneau(db, creneau_id)
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )
