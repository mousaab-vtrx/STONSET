"""GroupeTP API Router."""
from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.groupe_tp import GroupeTPCreate, GroupeTPUpdate, GroupeTPResponse
from app.services.groupe_tp_service import GroupeTPService
from app.repositories.groupe_tp_repo import GroupeTPRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/groupes-tp", tags=["groupes-tp"])


async def get_groupe_tp_service(db: AsyncSession = Depends(get_db)) -> GroupeTPService:
    """Dependency to get groupe_tp service."""
    from app.models.groupe_tp import GroupeTP
    repo = GroupeTPRepository(db, GroupeTP)
    return GroupeTPService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_groupe_tp(
    obj_in: GroupeTPCreate,
    current_user: User = Depends(require_role("responsable_service")),
    service: GroupeTPService = Depends(get_groupe_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new TP group. Only service managers can create groups."""
    try:
        groupe = await service.create_groupe_tp(db, obj_in)
        return success_response(data=GroupeTPResponse.from_orm(groupe).dict(), message="GroupeTP created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{groupe_id}", response_model=dict)
async def get_groupe_tp(
    groupe_id: int,
    service: GroupeTPService = Depends(get_groupe_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """Get TP group by ID."""
    try:
        groupe = await service.get_groupe_tp(db, groupe_id)
        return success_response(data=GroupeTPResponse.from_orm(groupe).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/module/{module_id}", response_model=dict)
async def get_groupes_by_module(
    module_id: int,
    service: GroupeTPService = Depends(get_groupe_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all TP groups in a module."""
    try:
        groupes = await service.get_groupes_by_module(db, module_id)
        return success_response(data=[GroupeTPResponse.from_orm(g).dict() for g in groupes])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/section/{section_id}", response_model=dict)
async def get_groupes_by_section(
    section_id: int,
    service: GroupeTPService = Depends(get_groupe_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all TP groups in a section."""
    try:
        groupes = await service.get_groupes_by_section(db, section_id)
        return success_response(data=[GroupeTPResponse.from_orm(g).dict() for g in groupes])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_groupes_tp(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    type: str = Query(None, description="Filter by session type: CM, TD, TP, EXAM, SEMINAR"),
    service: GroupeTPService = Depends(get_groupe_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """List all TP groups, optionally filtered by session type.
    
    Query parameters:
    - type: Optional session type (CM, TD, TP, EXAM, SEMINAR)
    - skip: Number of records to skip (default: 0)
    - limit: Number of records to return (default: 10, max: 100)
    """
    try:
        groupes = await service.get_all_groupes_tp(db, skip=skip, limit=limit, type_filter=type)
        return success_response(
            data=[GroupeTPResponse.from_orm(g).dict() for g in groupes],
            meta={"skip": skip, "limit": limit, "type_filter": type}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{groupe_id}", response_model=dict)
async def update_groupe_tp(
    groupe_id: int,
    obj_in: GroupeTPUpdate,
    current_user: User = Depends(require_role("responsable_service")),
    service: GroupeTPService = Depends(get_groupe_tp_service),
    db: AsyncSession = Depends(get_db)
):
    """Update TP group. Only service managers can update groups."""
    try:
        groupe = await service.update_groupe_tp(db, groupe_id, obj_in)
        return success_response(data=GroupeTPResponse.from_orm(groupe).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{groupe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_groupe_tp(
    groupe_id: int,
    current_user: User = Depends(require_role("responsable_service")),
    service: GroupeTPService = Depends(get_groupe_tp_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete TP group. Only service managers can delete groups."""
    try:
        await service.delete_groupe_tp(db, groupe_id)
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )
