import { create } from 'zustand'
import { reservationService } from '@/services/reservationService'
import type { Reservation, ReservationCreate, ReservationUpdate } from '@/types'

interface ReservationState {
  reservations: Reservation[]
  selectedReservation: Reservation | null
  isLoading: boolean
  error: string | null
  totalCount: number

  // Actions
  fetchReservations: (skip?: number, limit?: number) => Promise<void>
  fetchReservationById: (id: number) => Promise<void>
  createReservation: (data: ReservationCreate) => Promise<boolean>
  updateReservation: (id: number, data: ReservationUpdate) => Promise<boolean>
  deleteReservation: (id: number) => Promise<boolean>
  approveReservation: (id: number, etat_id: number) => Promise<boolean>
  rejectReservation: (id: number, etat_id: number) => Promise<boolean>
  clearError: () => void
}

export const useReservationStore = create<ReservationState>((set) => ({
  reservations: [],
  selectedReservation: null,
  isLoading: false,
  error: null,
  totalCount: 0,

  fetchReservations: async (skip = 0, limit = 100) => {
    set({ isLoading: true, error: null })
    try {
      const response = await reservationService.getAll(skip, limit)
      if (response.status === 'success' && Array.isArray(response.data)) {
        set({
          reservations: response.data,
          totalCount: response.meta?.total || response.data.length,
          isLoading: false,
        })
      } else {
        set({ error: response.message, isLoading: false })
      }
    } catch (err: any) {
      const message = err.response?.data?.message || 'Failed to fetch reservations'
      set({ error: message, isLoading: false })
    }
  },

  fetchReservationById: async (id: number) => {
    set({ isLoading: true, error: null })
    try {
      const response = await reservationService.getById(id)
      if (response.status === 'success' && response.data) {
        set({
          selectedReservation: response.data,
          isLoading: false,
        })
      } else {
        set({ error: response.message, isLoading: false })
      }
    } catch (err: any) {
      const message = err.response?.data?.message || 'Failed to fetch reservation'
      set({ error: message, isLoading: false })
    }
  },

  createReservation: async (data: ReservationCreate) => {
    set({ isLoading: true, error: null })
    try {
      const response = await reservationService.create(data)
      if (response.status === 'success' && response.data) {
        set((state) => ({
          reservations: [response.data as Reservation, ...state.reservations],
          isLoading: false,
        }))
        return true
      } else {
        set({ error: response.message, isLoading: false })
        return false
      }
    } catch (err: any) {
      const message = err.response?.data?.message || 'Failed to create reservation'
      set({ error: message, isLoading: false })
      return false
    }
  },

  updateReservation: async (id: number, data: ReservationUpdate) => {
    set({ isLoading: true, error: null })
    try {
      const response = await reservationService.update(id, data)
      if (response.status === 'success' && response.data) {
        set((state) => ({
          reservations: state.reservations.map((r) =>
            r.id === id ? response.data as Reservation : r
          ),
          selectedReservation:
            state.selectedReservation?.id === id
              ? (response.data as Reservation)
              : state.selectedReservation,
          isLoading: false,
        }))
        return true
      } else {
        set({ error: response.message, isLoading: false })
        return false
      }
    } catch (err: any) {
      const message = err.response?.data?.message || 'Failed to update reservation'
      set({ error: message, isLoading: false })
      return false
    }
  },

  deleteReservation: async (id: number) => {
    set({ isLoading: true, error: null })
    try {
      const response = await reservationService.delete(id)
      if (response.status === 'success') {
        set((state) => ({
          reservations: state.reservations.filter((r) => r.id !== id),
          selectedReservation:
            state.selectedReservation?.id === id ? null : state.selectedReservation,
          isLoading: false,
        }))
        return true
      } else {
        set({ error: response.message, isLoading: false })
        return false
      }
    } catch (err: any) {
      const message = err.response?.data?.message || 'Failed to delete reservation'
      set({ error: message, isLoading: false })
      return false
    }
  },

  approveReservation: async (id: number, etat_id: number) => {
    set({ isLoading: true, error: null })
    try {
      const response = await reservationService.approve(id, etat_id)
      if (response.status === 'success' && response.data) {
        set((state) => ({
          reservations: state.reservations.map((r) =>
            r.id === id ? response.data as Reservation : r
          ),
          isLoading: false,
        }))
        return true
      } else {
        set({ error: response.message, isLoading: false })
        return false
      }
    } catch (err: any) {
      const message = err.response?.data?.message || 'Failed to approve reservation'
      set({ error: message, isLoading: false })
      return false
    }
  },

  rejectReservation: async (id: number, etat_id: number) => {
    set({ isLoading: true, error: null })
    try {
      const response = await reservationService.reject(id, etat_id)
      if (response.status === 'success' && response.data) {
        set((state) => ({
          reservations: state.reservations.map((r) =>
            r.id === id ? response.data as Reservation : r
          ),
          isLoading: false,
        }))
        return true
      } else {
        set({ error: response.message, isLoading: false })
        return false
      }
    } catch (err: any) {
      const message = err.response?.data?.message || 'Failed to reject reservation'
      set({ error: message, isLoading: false })
      return false
    }
  },

  clearError: () => set({ error: null }),
}))
