"""Reservation Repository."""
from sqlmodel import Session, select, and_
from datetime import date
from typing import Optional
from app.models.reservation import Reservation
from app.repositories.base import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):
    """Repository for Reservation entity."""

    async def get_all(
        self,
        session: Session,
        skip: int = 0,
        limit: int = 100,
        *,
        etat_id: Optional[int] = None,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None,
        salle_id: Optional[int] = None,
        enseignant_id: Optional[int] = None,
        groupe_tp_id: Optional[int] = None,
    ) -> list[Reservation]:
        """Get reservations with optional filters."""
        query = select(Reservation)
        conditions = []
        if etat_id is not None:
            conditions.append(Reservation.etat_id == etat_id)
        if date_debut is not None:
            conditions.append(Reservation.date_seance >= date_debut)
        if date_fin is not None:
            conditions.append(Reservation.date_seance <= date_fin)
        if salle_id is not None:
            conditions.append(Reservation.salle_tp_id == salle_id)
        if enseignant_id is not None:
            conditions.append(Reservation.enseignant_id == enseignant_id)
        if groupe_tp_id is not None:
            conditions.append(Reservation.groupe_tp_id == groupe_tp_id)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.offset(skip).limit(limit).order_by(Reservation.date_seance.desc())
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, session: Session, obj_id: int) -> Reservation:
        """Get reservation by ID."""
        query = select(Reservation).where(Reservation.id == obj_id)
        result = await session.execute(query)
        return result.scalars().first()
    
    async def get_by_enseignant(self, session: Session, enseignant_id: int) -> list[Reservation]:
        """Get all reservations by a specific instructor."""
        query = select(Reservation).where(Reservation.enseignant_id == enseignant_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_salle(self, session: Session, salle_id: int) -> list[Reservation]:
        """Get all reservations for a specific room."""
        query = select(Reservation).where(Reservation.salle_tp_id == salle_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_etat(self, session: Session, etat_id: int) -> list[Reservation]:
        """Get reservations by status."""
        query = select(Reservation).where(Reservation.etat_id == etat_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_date_range(
        self, session: Session, start_date: date, end_date: date
    ) -> list[Reservation]:
        """Get reservations within a date range."""
        query = select(Reservation).where(
            (Reservation.date_seance >= start_date) & (Reservation.date_seance <= end_date)
        ).order_by(Reservation.date_seance)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_pending_reservations(self, session: Session) -> list[Reservation]:
        """Get pending (unapproved) reservations."""
        query = select(Reservation).where(
            Reservation.date_reponse.is_(None)
        ).order_by(Reservation.date_demande)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_creneau(self, session: Session, creneau_id: int) -> list[Reservation]:
        """Get reservations for a specific time slot."""
        query = select(Reservation).where(Reservation.creneau_id == creneau_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_groupe_tp(self, session: Session, groupe_tp_id: int) -> list[Reservation]:
        """Get reservations for a specific TP group."""
        query = select(Reservation).where(Reservation.groupe_tp_id == groupe_tp_id)
        result = await session.execute(query)
        return result.scalars().all()
