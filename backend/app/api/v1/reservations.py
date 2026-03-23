"""Reservation API Router."""
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional
from app.api.deps import get_db, get_current_user, require_role
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationResponse
from app.services.reservation_service import ReservationService
from app.repositories.reservation_repo import ReservationRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/reservations", tags=["reservations"])


async def get_reservation_service(db: AsyncSession = Depends(get_db)) -> ReservationService:
    """Dependency to get reservation service."""
    from app.models.reservation import Reservation
    repo = ReservationRepository(db, Reservation)
    return ReservationService(repo)


@router.get("", response_model=dict)
async def list_reservations(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    etat_id: Optional[int] = Query(None, description="Filter by status ID"),
    date_debut: Optional[date] = Query(None, description="Filter by session start date"),
    date_fin: Optional[date] = Query(None, description="Filter by session end date"),
    salle_id: Optional[int] = Query(None, description="Filter by room ID"),
    enseignant_id: Optional[int] = Query(None, description="Filter by instructor ID"),
    groupe_tp_id: Optional[int] = Query(None, description="Filter by TP group ID"),
    current_user: User = Depends(get_current_user),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """List reservations. Enseignant sees only their own; responsable_service and chef_dept see all."""
    try:
        filters = {
            "etat_id": etat_id,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "salle_id": salle_id,
            "enseignant_id": enseignant_id,
            "groupe_tp_id": groupe_tp_id,
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        if current_user.user_type == "enseignant":
            filters["enseignant_id"] = current_user.id

        reservations = await service.get_all_reservations(
            db, skip=skip, limit=limit, **filters
        )
        return success_response(
            data=[ReservationResponse.from_orm(r).dict() for r in reservations],
            meta={"skip": skip, "limit": limit}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    obj_in: ReservationCreate,
    current_user: User = Depends(get_current_user),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new reservation request. Requires authentication."""
    try:
        reservation = await service.create_reservation(db, obj_in)
        return success_response(
            data=ReservationResponse.from_orm(reservation).dict(),
            message="Reservation created successfully"
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/enseignant/{enseignant_id}", response_model=dict)
async def get_reservations_by_enseignant(
    enseignant_id: int,
    current_user: User = Depends(get_current_user),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all reservations by an instructor. Requires authentication."""
    try:
        reservations = await service.get_reservations_by_enseignant(db, enseignant_id)
        return success_response(data=[ReservationResponse.from_orm(r).dict() for r in reservations])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/salle/{salle_id}", response_model=dict)
async def get_reservations_by_salle(
    salle_id: int,
    current_user: User = Depends(get_current_user),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all reservations for a room. Requires authentication."""
    try:
        reservations = await service.get_reservations_by_salle(db, salle_id)
        return success_response(data=[ReservationResponse.from_orm(r).dict() for r in reservations])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/etat/{etat_id}", response_model=dict)
async def get_reservations_by_etat(
    etat_id: int,
    current_user: User = Depends(get_current_user),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """Get reservations by status. Requires authentication."""
    try:
        reservations = await service.get_reservations_by_etat(db, etat_id)
        return success_response(data=[ReservationResponse.from_orm(r).dict() for r in reservations])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/pending", response_model=dict)
async def get_pending_reservations(
    current_user: User = Depends(require_role("responsable_service")),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """Get pending (unapproved) reservations. Only responsable_service can view pending."""
    try:
        reservations = await service.get_pending_reservations(db)
        return success_response(data=[ReservationResponse.from_orm(r).dict() for r in reservations])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/date-range/{start_date}/{end_date}", response_model=dict)
async def get_reservations_by_date_range(
    start_date: date,
    end_date: date,
    current_user: User = Depends(get_current_user),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """Get reservations within date range. Requires authentication."""
    try:
        reservations = await service.get_reservations_by_date_range(db, start_date, end_date)
        return success_response(data=[ReservationResponse.from_orm(r).dict() for r in reservations])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{reservation_id}", response_model=dict)
async def get_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_user),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """Get reservation by ID. Enseignant sees only own; responsable/chef see all."""
    try:
        reservation = await service.get_reservation(db, reservation_id, current_user)
        return success_response(data=ReservationResponse.from_orm(reservation).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{reservation_id}", response_model=dict)
async def update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    current_user: User = Depends(get_current_user),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """Update reservation. Enseignant can only update own."""
    try:
        reservation = await service.update_reservation(
            db, reservation_id, obj_in, current_user
        )
        return success_response(data=ReservationResponse.from_orm(reservation).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.post("/{reservation_id}/approve/{etat_id}", response_model=dict)
async def approve_reservation(
    reservation_id: int,
    etat_id: int,
    current_user: User = Depends(require_role("responsable_service")),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """Approve a reservation request. Only responsable_service can approve."""
    try:
        reservation = await service.approve_reservation(db, reservation_id, etat_id)
        return success_response(
            data=ReservationResponse.from_orm(reservation).dict(),
            message="Reservation approved"
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.post("/{reservation_id}/reject/{etat_id}", response_model=dict)
async def reject_reservation(
    reservation_id: int,
    etat_id: int,
    current_user: User = Depends(require_role("responsable_service")),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
):
    """Reject a reservation request. Only responsable_service can reject."""
    try:
        reservation = await service.reject_reservation(db, reservation_id, etat_id)
        return success_response(
            data=ReservationResponse.from_orm(reservation).dict(),
            message="Reservation rejected"
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_user),
    service: ReservationService = Depends(get_reservation_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete reservation. Enseignant can only delete own."""
    try:
        await service.delete_reservation(db, reservation_id, current_user)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
