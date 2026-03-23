"""Etat (Status) API Router."""
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.etat import EtatCreate, EtatUpdate, EtatResponse
from app.services.etat_service import EtatService
from app.repositories.etat_repo import EtatRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/etats", tags=["etats"])


async def get_etat_service(db: AsyncSession = Depends(get_db)) -> EtatService:
    """Dependency to get etat service."""
    from app.models.etat import Etat
    repo = EtatRepository(db, Etat)
    return EtatService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_etat(
    obj_in: EtatCreate,
    current_user: User = Depends(require_role("responsable_service")),
    service: EtatService = Depends(get_etat_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new status. Only responsable_service can create statuses."""
    try:
        etat = await service.create_etat(db, obj_in)
        return success_response(data=EtatResponse.from_orm(etat).dict(), message="Status created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{etat_id}", response_model=dict)
async def get_etat(
    etat_id: int,
    current_user: User = Depends(get_current_user),
    service: EtatService = Depends(get_etat_service),
    db: AsyncSession = Depends(get_db)
):
    """Get status by ID. Requires authentication."""
    try:
        etat = await service.get_etat(db, etat_id)
        return success_response(data=EtatResponse.from_orm(etat).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_etats(
    current_user: User = Depends(get_current_user),
    service: EtatService = Depends(get_etat_service),
    db: AsyncSession = Depends(get_db)
):
    """List all statuses. Requires authentication."""
    try:
        etats = await service.get_all_etats(db)
        return success_response(data=[EtatResponse.from_orm(e).dict() for e in etats])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{etat_id}", response_model=dict)
async def update_etat(
    etat_id: int,
    obj_in: EtatUpdate,
    current_user: User = Depends(require_role("responsable_service")),
    service: EtatService = Depends(get_etat_service),
    db: AsyncSession = Depends(get_db)
):
    """Update status. Only responsable_service can update statuses."""
    try:
        etat = await service.update_etat(db, etat_id, obj_in)
        return success_response(data=EtatResponse.from_orm(etat).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{etat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_etat(
    etat_id: int,
    current_user: User = Depends(require_role("responsable_service")),
    service: EtatService = Depends(get_etat_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete status. Only responsable_service can delete statuses."""
    try:
        await service.delete_etat(db, etat_id)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
