"""Niveau (Academic Level) API Router."""
from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.niveau import NiveauCreate, NiveauUpdate, NiveauResponse
from app.services.niveau_service import NiveauService
from app.repositories.niveau_repo import NiveauRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/niveaux", tags=["niveaux"])


async def get_niveau_service(db: AsyncSession = Depends(get_db)) -> NiveauService:
    """Dependency to get niveau service."""
    from app.models.niveau import Niveau
    repo = NiveauRepository(db, Niveau)
    return NiveauService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_niveau(
    obj_in: NiveauCreate,
    service: NiveauService = Depends(get_niveau_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new academic level."""
    try:
        niveau = await service.create_niveau(db, obj_in)
        return success_response(data=NiveauResponse.from_orm(niveau).dict(), message="Niveau created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{niveau_id}", response_model=dict)
async def get_niveau(
    niveau_id: int,
    service: NiveauService = Depends(get_niveau_service),
    db: AsyncSession = Depends(get_db)
):
    """Get academic level by ID."""
    try:
        niveau = await service.get_niveau(db, niveau_id)
        return success_response(data=NiveauResponse.from_orm(niveau).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/department/{department_id}", response_model=dict)
async def get_niveaux_by_department(
    department_id: int,
    service: NiveauService = Depends(get_niveau_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all levels in a department."""
    try:
        niveaux = await service.get_niveaux_by_department(db, department_id)
        return success_response(data=[NiveauResponse.from_orm(n).dict() for n in niveaux])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_niveaux(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: NiveauService = Depends(get_niveau_service),
    db: AsyncSession = Depends(get_db)
):
    """List all academic levels."""
    try:
        niveaux = await service.get_all_niveaux(db, skip=skip, limit=limit)
        return success_response(
            data=[NiveauResponse.from_orm(n).dict() for n in niveaux],
            meta={"skip": skip, "limit": limit}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{niveau_id}", response_model=dict)
async def update_niveau(
    niveau_id: int,
    obj_in: NiveauUpdate,
    service: NiveauService = Depends(get_niveau_service),
    db: AsyncSession = Depends(get_db)
):
    """Update academic level."""
    try:
        niveau = await service.update_niveau(db, niveau_id, obj_in)
        return success_response(data=NiveauResponse.from_orm(niveau).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{niveau_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_niveau(
    niveau_id: int,
    current_user: User = Depends(require_role("chef_dept", "responsable_service")),
    service: NiveauService = Depends(get_niveau_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete academic level. Only chef_dept and responsable_service can delete levels."""
    try:
        await service.delete_niveau(db, niveau_id)
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )
