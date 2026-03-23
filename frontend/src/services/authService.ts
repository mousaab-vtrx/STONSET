import apiClient from './apiClient'
import type {
  ApiResponse,
  User,
  LoginRequest,
  RegisterRequest,
  AuthResponse,
} from '@/types'

export const authService = {
  login: async (credentials: LoginRequest): Promise<ApiResponse<AuthResponse>> => {
    const response = await apiClient.post<ApiResponse<AuthResponse>>(
      '/api/v1/auth/login',
      credentials
    )
    return response.data
  },

  register: async (data: RegisterRequest): Promise<ApiResponse<AuthResponse>> => {
    const response = await apiClient.post<ApiResponse<AuthResponse>>(
      '/api/v1/auth/register',
      data
    )
    return response.data
  },

  refreshToken: async (refreshToken: string): Promise<ApiResponse<AuthResponse>> => {
    const response = await apiClient.post<ApiResponse<AuthResponse>>(
      '/api/v1/auth/refresh-token',
      { refresh_token: refreshToken }
    )
    return response.data
  },

  logout: async (): Promise<ApiResponse<null>> => {
    const response = await apiClient.post<ApiResponse<null>>('/api/v1/auth/logout')
    return response.data
  },

  getCurrentUser: async (): Promise<ApiResponse<User>> => {
    const response = await apiClient.get<ApiResponse<User>>('/api/v1/account/auth/me')
    return response.data
  },

  updateProfile: async (_data: Partial<User>): Promise<ApiResponse<User>> => {
    // TODO: Implement profile update endpoint in backend - currently not available
    // This endpoint should be implemented at /api/v1/account/update or /api/v1/users/me
    throw new Error('Profile update endpoint not yet implemented in backend')
  },

  deleteAccount: async (feedback: { reason: string; additional_feedback?: string }): Promise<ApiResponse<null>> => {
    const response = await apiClient.post<ApiResponse<null>>(
      '/api/v1/account/delete',
      feedback
    )
    return response.data
  },

  uploadAvatar: async (file: File): Promise<ApiResponse<{ avatar_url: string }>> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await apiClient.post<ApiResponse<{ avatar_url: string }>>(
      '/api/v1/avatars/upload',
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )
    return response.data
  },
}
