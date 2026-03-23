"""Filière API Router."""
from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.filiere import FiliereCreate, FiliereUpdate, FiliereResponse
from app.services.filiere_service import FiliereService
from app.repositories.filiere_repo import FiliereRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/filieres", tags=["filieres"])


async def get_filiere_service(db: AsyncSession = Depends(get_db)) -> FiliereService:
    """Dependency to get filiere service."""
    from app.models.filiere import Filiere
    repo = FiliereRepository(db, Filiere)
    return FiliereService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_filiere(
    obj_in: FiliereCreate,
    service: FiliereService = Depends(get_filiere_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new academic program."""
    try:
        filiere = await service.create_filiere(db, obj_in)
        return success_response(data=FiliereResponse.from_orm(filiere).dict(), message="Filière created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{filiere_id}", response_model=dict)
async def get_filiere(
    filiere_id: int,
    service: FiliereService = Depends(get_filiere_service),
    db: AsyncSession = Depends(get_db)
):
    """Get academic program by ID."""
    try:
        filiere = await service.get_filiere(db, filiere_id)
        return success_response(data=FiliereResponse.from_orm(filiere).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/niveau/{niveau_id}", response_model=dict)
async def get_filieres_by_niveau(
    niveau_id: int,
    service: FiliereService = Depends(get_filiere_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all programs in a level."""
    try:
        filieres = await service.get_filieres_by_niveau(db, niveau_id)
        return success_response(data=[FiliereResponse.from_orm(f).dict() for f in filieres])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_filieres(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: FiliereService = Depends(get_filiere_service),
    db: AsyncSession = Depends(get_db)
):
    """List all academic programs."""
    try:
        filieres = await service.get_all_filieres(db, skip=skip, limit=limit)
        return success_response(
            data=[FiliereResponse.from_orm(f).dict() for f in filieres],
            meta={"skip": skip, "limit": limit}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{filiere_id}", response_model=dict)
async def update_filiere(
    filiere_id: int,
    obj_in: FiliereUpdate,
    service: FiliereService = Depends(get_filiere_service),
    db: AsyncSession = Depends(get_db)
):
    """Update academic program."""
    try:
        filiere = await service.update_filiere(db, filiere_id, obj_in)
        return success_response(data=FiliereResponse.from_orm(filiere).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{filiere_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_filiere(
    filiere_id: int,
    current_user: User = Depends(require_role("chef_dept", "responsable_service")),
    service: FiliereService = Depends(get_filiere_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete academic program. Only chef_dept and responsable_service can delete programs."""
    try:
        await service.delete_filiere(db, filiere_id)
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )
