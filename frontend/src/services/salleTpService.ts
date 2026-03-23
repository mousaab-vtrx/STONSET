import apiClient from './apiClient'
import type { ApiResponse, SalleTP } from '@/types'

export const salleTpService = {
  getAll: async (skip = 0, limit = 100): Promise<ApiResponse<SalleTP[]>> => {
    const response = await apiClient.get<ApiResponse<SalleTP[]>>(
      '/api/v1/salles-tp',
      { params: { skip, limit } }
    )
    return response.data
  },

  getById: async (id: number): Promise<ApiResponse<SalleTP>> => {
    const response = await apiClient.get<ApiResponse<SalleTP>>(
      `/api/v1/salles-tp/${id}`
    )
    return response.data
  },

  create: async (data: Partial<SalleTP>): Promise<ApiResponse<SalleTP>> => {
    const response = await apiClient.post<ApiResponse<SalleTP>>(
      '/api/v1/salles-tp',
      data
    )
    return response.data
  },

  update: async (id: number, data: Partial<SalleTP>): Promise<ApiResponse<SalleTP>> => {
    const response = await apiClient.put<ApiResponse<SalleTP>>(
      `/api/v1/salles-tp/${id}`,
      data
    )
    return response.data
  },

  delete: async (id: number): Promise<ApiResponse<null>> => {
    const response = await apiClient.delete<ApiResponse<null>>(
      `/api/v1/salles-tp/${id}`
    )
    return response.data
  },
}
