"""SalleTP (TP Room) API Router."""
from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.salle_tp import SalleTPCreate, SalleTPUpdate, SalleTPResponse
from app.services.salle_tp_service import SalleTPService
from app.repositories.salle_tp_repo import SalleTPRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/salles-tp", tags=["salles-tp"])


async def get_salle_tp_service(db: AsyncSession = Depends(get_db)) -> SalleTPService:
    """Dependency to get salle_tp service."""
    from app.models.salle_tp import SalleTP
    repo = SalleTPRepository(db, SalleTP)
    return SalleTPService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_salle_tp(
    obj_in: SalleTPCreate,
    current_user: User = Depends(require_role("responsable_service")),
    service: SalleTPService = Depends(get_salle_tp_service),
    db: AsyncSession = Depends(get_db),
):
    """Create a new TP room. Only responsable_service can create rooms."""
    try:
        salle = await service.create_salle_tp(db, obj_in)
        return success_response(data=SalleTPResponse.from_orm(salle).dict(), message="SalleTP created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{salle_id}", response_model=dict)
async def get_salle_tp(
    salle_id: int,
    service: SalleTPService = Depends(get_salle_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """Get TP room by ID."""
    try:
        salle = await service.get_salle_tp(db, salle_id)
        return success_response(data=SalleTPResponse.from_orm(salle).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/active", response_model=dict)
async def get_active_rooms(
    service: SalleTPService = Depends(get_salle_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all active rooms."""
    try:
        salles = await service.get_active_rooms(db)
        return success_response(data=[SalleTPResponse.from_orm(s).dict() for s in salles])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/capacity/{min_capacity}", response_model=dict)
async def get_rooms_by_capacity(
    min_capacity: int,
    service: SalleTPService = Depends(get_salle_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """Get rooms with minimum capacity."""
    try:
        salles = await service.get_rooms_by_capacity(db, min_capacity)
        return success_response(data=[SalleTPResponse.from_orm(s).dict() for s in salles])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/with-internet", response_model=dict)
async def get_rooms_with_internet(
    service: SalleTPService = Depends(get_salle_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """Get rooms with internet access."""
    try:
        salles = await service.get_rooms_with_internet(db)
        return success_response(data=[SalleTPResponse.from_orm(s).dict() for s in salles])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/with-projector", response_model=dict)
async def get_rooms_with_projector(
    service: SalleTPService = Depends(get_salle_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """Get rooms with projector."""
    try:
        salles = await service.get_rooms_with_projector(db)
        return success_response(data=[SalleTPResponse.from_orm(s).dict() for s in salles])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_salles_tp(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: SalleTPService = Depends(get_salle_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """List all TP rooms."""
    try:
        salles = await service.get_all_salles_tp(db, skip=skip, limit=limit)
        return success_response(
            data=[SalleTPResponse.from_orm(s).dict() for s in salles],
            meta={"skip": skip, "limit": limit}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{salle_id}", response_model=dict)
async def update_salle_tp(
    salle_id: int,
    obj_in: SalleTPUpdate,
    current_user: User = Depends(require_role("responsable_service")),
    service: SalleTPService = Depends(get_salle_tp_service),
    db: AsyncSession = Depends(get_db),
):
    """Update TP room. Only responsable_service can update rooms."""
    try:
        salle = await service.update_salle_tp(db, salle_id, obj_in)
        return success_response(data=SalleTPResponse.from_orm(salle).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{salle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_salle_tp(
    salle_id: int,
    current_user: User = Depends(require_role("responsable_service")),
    service: SalleTPService = Depends(get_salle_tp_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete TP room. Only responsable_service can delete rooms."""
    try:
        await service.delete_salle_tp(db, salle_id)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
