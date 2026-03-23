import { useReservationStore } from '@/store/reservationStore'
import type { ReservationCreate, ReservationUpdate } from '@/types'

export const useReservation = () => {
  const store = useReservationStore()

  const fetchReservations = async (skip = 0, limit = 100) => {
    return store.fetchReservations(skip, limit)
  }

  const fetchReservationById = async (id: number) => {
    return store.fetchReservationById(id)
  }

  const createReservation = async (data: ReservationCreate) => {
    return store.createReservation(data)
  }

  const updateReservation = async (id: number, data: ReservationUpdate) => {
    return store.updateReservation(id, data)
  }

  const deleteReservation = async (id: number) => {
    return store.deleteReservation(id)
  }

  const approveReservation = async (id: number, etat_id: number) => {
    return store.approveReservation(id, etat_id)
  }

  const rejectReservation = async (id: number, etat_id: number) => {
    return store.rejectReservation(id, etat_id)
  }

  return {
    reservations: store.reservations,
    selectedReservation: store.selectedReservation,
    isLoading: store.isLoading,
    error: store.error,
    totalCount: store.totalCount,
    fetchReservations,
    fetchReservationById,
    createReservation,
    updateReservation,
    deleteReservation,
    approveReservation,
    rejectReservation,
    clearError: store.clearError,
  }
}
