"""Reservation Service."""
from datetime import date
from typing import Optional
from sqlmodel import Session
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from app.repositories.reservation_repo import ReservationRepository
from app.core.exceptions import NotFoundError, ConflictError, ForbiddenException


class ReservationService:
    """Service for reservation operations."""
    
    def __init__(self, repo: ReservationRepository):
        self.repo = repo
    
    async def create_reservation(self, session: Session, obj_in: ReservationCreate) -> Reservation:
        """Create a new reservation request."""
        db_obj = Reservation.from_orm(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    def _can_access_reservation(self, user: User, reservation: Reservation) -> bool:
        """Check if user can access this reservation (own or has elevated role)."""
        if user.user_type in ("responsable_service", "chef_dept"):
            return True
        return reservation.enseignant_id == user.id

    async def get_reservation(
        self, session: Session, reservation_id: int, current_user: Optional[User] = None
    ) -> Reservation:
        """Get reservation by ID. Enseignant can only access own reservations."""
        db_obj = await self.repo.get_by_id(session, reservation_id)
        if not db_obj:
            raise NotFoundError(f"Reservation with ID {reservation_id} not found")
        if current_user and not self._can_access_reservation(current_user, db_obj):
            raise ForbiddenException("You do not have access to this reservation")
        return db_obj

    async def get_reservations_by_enseignant(self, session: Session, enseignant_id: int) -> list[Reservation]:
        """Get all reservations by an instructor."""
        return await self.repo.get_by_enseignant(session, enseignant_id)
    
    async def get_reservations_by_salle(self, session: Session, salle_id: int) -> list[Reservation]:
        """Get all reservations for a room."""
        return await self.repo.get_by_salle(session, salle_id)
    
    async def get_reservations_by_etat(self, session: Session, etat_id: int) -> list[Reservation]:
        """Get reservations by status."""
        return await self.repo.get_by_etat(session, etat_id)
    
    async def get_reservations_by_date_range(
        self, session: Session, start_date: date, end_date: date
    ) -> list[Reservation]:
        """Get reservations within date range."""
        return await self.repo.get_by_date_range(session, start_date, end_date)
    
    async def get_pending_reservations(self, session: Session) -> list[Reservation]:
        """Get pending (unapproved) reservations."""
        return await self.repo.get_pending_reservations(session)
    
    async def get_all_reservations(
        self,
        session: Session,
        skip: int = 0,
        limit: int = 10,
        *,
        etat_id: Optional[int] = None,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None,
        salle_id: Optional[int] = None,
        enseignant_id: Optional[int] = None,
        groupe_tp_id: Optional[int] = None,
    ) -> list[Reservation]:
        """Get reservations with optional filters."""
        return await self.repo.get_all(
            session,
            skip=skip,
            limit=limit,
            etat_id=etat_id,
            date_debut=date_debut,
            date_fin=date_fin,
            salle_id=salle_id,
            enseignant_id=enseignant_id,
            groupe_tp_id=groupe_tp_id,
        )
    
    async def update_reservation(
        self,
        session: Session,
        reservation_id: int,
        obj_in: ReservationUpdate,
        current_user: Optional[User] = None,
    ) -> Reservation:
        """Update reservation. Enseignant can only update own reservations."""
        db_obj = await self.get_reservation(session, reservation_id, current_user)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def approve_reservation(self, session: Session, reservation_id: int, etat_id: int) -> Reservation:
        """Approve a reservation request."""
        from datetime import datetime
        db_obj = await self.get_reservation(session, reservation_id)
        db_obj.etat_id = etat_id
        db_obj.date_reponse = datetime.utcnow()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def reject_reservation(self, session: Session, reservation_id: int, etat_id: int) -> Reservation:
        """Reject a reservation request."""
        from datetime import datetime
        db_obj = await self.get_reservation(session, reservation_id)
        db_obj.etat_id = etat_id
        db_obj.date_reponse = datetime.utcnow()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete_reservation(
        self, session: Session, reservation_id: int, current_user: Optional[User] = None
    ) -> None:
        """Delete reservation. Enseignant can only delete own reservations."""
        db_obj = await self.get_reservation(session, reservation_id, current_user)
        await session.delete(db_obj)
        await session.commit()
    
    async def commit(self, session: Session) -> None:
        """Commit transaction."""
        await session.commit()
