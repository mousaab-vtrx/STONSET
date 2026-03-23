"""Vacances API Router."""
from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.vacances import VacancesCreate, VacancesUpdate, VacancesResponse
from app.services.vacances_service import VacancesService
from app.repositories.vacances_repo import VacancesRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/vacances", tags=["vacances"])


async def get_vacances_service(db: AsyncSession = Depends(get_db)) -> VacancesService:
    """Dependency to get vacances service."""
    from app.models.vacances import Vacances
    repo = VacancesRepository(db, Vacances)
    return VacancesService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_vacances(
    obj_in: VacancesCreate,
    current_user: User = Depends(require_role("responsable_service")),
    service: VacancesService = Depends(get_vacances_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new vacation period. Only responsable_service can create vacations."""
    try:
        vacances = await service.create_vacances(db, obj_in)
        return success_response(data=VacancesResponse.from_orm(vacances).dict(), message="Vacances created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{vacances_id}", response_model=dict)
async def get_vacances(
    vacances_id: int,
    service: VacancesService = Depends(get_vacances_service),
    db: AsyncSession = Depends(get_db)
):
    """Get vacation period by ID."""
    try:
        vacances = await service.get_vacances(db, vacances_id)
        return success_response(data=VacancesResponse.from_orm(vacances).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/active/{current_date}", response_model=dict)
async def get_active_vacations(
    current_date: date,
    service: VacancesService = Depends(get_vacances_service),
    db: AsyncSession = Depends(get_db)
):
    """Get currently active vacation periods."""
    try:
        vacances_list = await service.get_active_vacations(db, current_date)
        return success_response(data=[VacancesResponse.from_orm(v).dict() for v in vacances_list])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/upcoming/{from_date}", response_model=dict)
async def get_upcoming_vacations(
    from_date: date,
    service: VacancesService = Depends(get_vacances_service),
    db: AsyncSession = Depends(get_db)
):
    """Get upcoming vacation periods."""
    try:
        vacances_list = await service.get_upcoming_vacations(db, from_date)
        return success_response(data=[VacancesResponse.from_orm(v).dict() for v in vacances_list])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_vacances(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: VacancesService = Depends(get_vacances_service),
    db: AsyncSession = Depends(get_db)
):
    """List all vacation periods."""
    try:
        vacances_list = await service.get_all_vacances(db, skip=skip, limit=limit)
        return success_response(
            data=[VacancesResponse.from_orm(v).dict() for v in vacances_list],
            meta={"skip": skip, "limit": limit}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{vacances_id}", response_model=dict)
async def update_vacances(
    vacances_id: int,
    obj_in: VacancesUpdate,
    service: VacancesService = Depends(get_vacances_service),
    db: AsyncSession = Depends(get_db)
):
    """Update vacation period."""
    try:
        vacances = await service.update_vacances(db, vacances_id, obj_in)
        return success_response(data=VacancesResponse.from_orm(vacances).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{vacances_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacances(
    vacances_id: int,
    current_user: User = Depends(require_role("responsable_service")),
    service: VacancesService = Depends(get_vacances_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete vacation period. Only responsable_service can delete vacations."""
    try:
        await service.delete_vacances(db, vacances_id)
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )
