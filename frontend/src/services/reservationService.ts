import apiClient from './apiClient'
import type {
  ApiResponse,
  Reservation,
  ReservationCreate,
  ReservationUpdate,
} from '@/types'

export const reservationService = {
  getAll: async (skip = 0, limit = 100): Promise<ApiResponse<Reservation[]>> => {
    const response = await apiClient.get<ApiResponse<Reservation[]>>(
      '/api/v1/reservations',
      { params: { skip, limit } }
    )
    return response.data
  },

  getById: async (id: number): Promise<ApiResponse<Reservation>> => {
    const response = await apiClient.get<ApiResponse<Reservation>>(
      `/api/v1/reservations/${id}`
    )
    return response.data
  },

  create: async (data: ReservationCreate): Promise<ApiResponse<Reservation>> => {
    const response = await apiClient.post<ApiResponse<Reservation>>(
      '/api/v1/reservations',
      data
    )
    return response.data
  },

  update: async (id: number, data: ReservationUpdate): Promise<ApiResponse<Reservation>> => {
    const response = await apiClient.put<ApiResponse<Reservation>>(
      `/api/v1/reservations/${id}`,
      data
    )
    return response.data
  },

  delete: async (id: number): Promise<ApiResponse<null>> => {
    const response = await apiClient.delete<ApiResponse<null>>(
      `/api/v1/reservations/${id}`
    )
    return response.data
  },

  approve: async (id: number, etat_id: number): Promise<ApiResponse<Reservation>> => {
    const response = await apiClient.post<ApiResponse<Reservation>>(
      `/api/v1/reservations/${id}/approve/${etat_id}`
    )
    return response.data
  },

  reject: async (id: number, etat_id: number): Promise<ApiResponse<Reservation>> => {
    const response = await apiClient.post<ApiResponse<Reservation>>(
      `/api/v1/reservations/${id}/reject/${etat_id}`
    )
    return response.data
  },

  getByEnseignant: async (enseignant_id: number, skip = 0, limit = 100): Promise<ApiResponse<Reservation[]>> => {
    const response = await apiClient.get<ApiResponse<Reservation[]>>(
      `/api/v1/reservations/enseignant/${enseignant_id}`,
      { params: { skip, limit } }
    )
    return response.data
  },

  getBySalle: async (salle_id: number, skip = 0, limit = 100): Promise<ApiResponse<Reservation[]>> => {
    const response = await apiClient.get<ApiResponse<Reservation[]>>(
      `/api/v1/reservations/salle/${salle_id}`,
      { params: { skip, limit } }
    )
    return response.data
  },

  getByEtat: async (etat_id: number, skip = 0, limit = 100): Promise<ApiResponse<Reservation[]>> => {
    const response = await apiClient.get<ApiResponse<Reservation[]>>(
      `/api/v1/reservations/etat/${etat_id}`,
      { params: { skip, limit } }
    )
    return response.data
  },

  getPending: async (skip = 0, limit = 100): Promise<ApiResponse<Reservation[]>> => {
    const response = await apiClient.get<ApiResponse<Reservation[]>>(
      `/api/v1/reservations/pending`,
      { params: { skip, limit } }
    )
    return response.data
  },

  getByDateRange: async (start_date: string, end_date: string, skip = 0, limit = 100): Promise<ApiResponse<Reservation[]>> => {
    const response = await apiClient.get<ApiResponse<Reservation[]>>(
      `/api/v1/reservations/date-range/${start_date}/${end_date}`,
      { params: { skip, limit } }
    )
    return response.data
  },
}
