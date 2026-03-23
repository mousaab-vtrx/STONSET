import { create } from 'zustand'
import { authService } from '@/services/authService'
import type { User } from '@/types'

interface AuthState {
  // State
  user: User | null
  token: string | null
  refreshToken: string | null
  isLoading: boolean
  error: string | null
  isLoggedIn: boolean
  userAvatar: string | null

  // Computed properties
  userType: string | null
  isEnseignant: boolean
  isChefDept: boolean
  isResponsableService: boolean

  // Actions
  login: (email: string, password: string) => Promise<boolean>
  register: (email: string, password: string, firstName: string, lastName: string) => Promise<boolean>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  restoreSession: () => Promise<void>
  refreshAuthToken: () => Promise<boolean>
  updateProfile: (data: Partial<User>) => Promise<boolean>
  clearError: () => void
  uploadAvatar: (file: File) => Promise<boolean>
}

export const useAuthStore = create<AuthState>((set, get) => ({
  // State
  user: null,
  token: localStorage.getItem('access_token'),
  refreshToken: localStorage.getItem('refresh_token'),
  isLoading: false,
  error: null,
  isLoggedIn: !!localStorage.getItem('access_token'),
  userAvatar: null,

  // Computed properties
  userType: null,
  isEnseignant: false,
  isChefDept: false,
  isResponsableService: false,

  login: async (email: string, password: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authService.login({ email, password })
      console.log('Login response:', response)

      if (response.status === 'success' && response.data) {
        console.log('Login successful, setting state')
        localStorage.setItem('access_token', response.data.access_token)
        if (response.data.refresh_token) {
          localStorage.setItem('refresh_token', response.data.refresh_token)
        }
        localStorage.setItem('user', JSON.stringify(response.data.user))

        const state = {
          user: response.data.user,
          token: response.data.access_token,
          refreshToken: response.data.refresh_token || null,
          isLoggedIn: true,
          isLoading: false,
          userAvatar: response.data.user.avatar_url || null,
          userType: response.data.user.user_type,
          isEnseignant: response.data.user.user_type === 'enseignant',
          isChefDept: response.data.user.user_type === 'chef_dept',
          isResponsableService: response.data.user.user_type === 'responsable_service',
        }
        set(state)
        console.log('State updated, isLoggedIn should be true now')
        return true
      } else {
        console.log('Response status not success:', response.status)
        const message = response.message || 'Login failed'
        set({ error: message, isLoading: false })
        return false
      }
    } catch (err: any) {
      console.error('Login error:', err)
      const message = err.response?.data?.message || 'An error occurred during login'
      set({ error: message, isLoading: false })
      return false
    }
  },

  register: async (email: string, password: string, prenom_user: string, nom_user: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authService.register({
        email,
        password,
        nom_user,
        prenom_user,
      })
      if (response.status === 'success' && response.data) {
        localStorage.setItem('access_token', response.data.access_token)
        if (response.data.refresh_token) {
          localStorage.setItem('refresh_token', response.data.refresh_token)
        }
        localStorage.setItem('user', JSON.stringify(response.data.user))

        const state = {
          user: response.data.user,
          token: response.data.access_token,
          refreshToken: response.data.refresh_token || null,
          isLoggedIn: true,
          isLoading: false,
          userAvatar: response.data.user.avatar_url || null,
          userType: response.data.user.user_type,
          isEnseignant: response.data.user.user_type === 'enseignant',
          isChefDept: response.data.user.user_type === 'chef_dept',
          isResponsableService: response.data.user.user_type === 'responsable_service',
        }
        set(state)
        return true
      } else {
        const message = response.message || 'Registration failed'
        set({ error: message, isLoading: false })
        return false
      }
    } catch (err: any) {
      const message = err.response?.data?.message || 'An error occurred during registration'
      set({ error: message, isLoading: false })
      return false
    }
  },

  logout: async () => {
    try {
      await authService.logout()
    } catch {
      // Ignore network errors on logout
    }
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    set({
      user: null,
      token: null,
      refreshToken: null,
      isLoggedIn: false,
      error: null,
      userAvatar: null,
      userType: null,
      isEnseignant: false,
      isChefDept: false,
      isResponsableService: false,
    })
  },

  checkAuth: async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      set({ isLoggedIn: false })
      return
    }

    try {
      const response = await authService.getCurrentUser()
      if (response.status === 'success' && response.data) {
        const state = {
          user: response.data,
          isLoggedIn: true,
          userAvatar: response.data.avatar_url || null,
          userType: response.data.user_type,
          isEnseignant: response.data.user_type === 'enseignant',
          isChefDept: response.data.user_type === 'chef_dept',
          isResponsableService: response.data.user_type === 'responsable_service',
        }
        set(state)
      } else {
        set({ isLoggedIn: false })
      }
    } catch {
      set({ isLoggedIn: false })
    }
  },

  restoreSession: async () => {
    const token = localStorage.getItem('access_token')
    const refreshToken = localStorage.getItem('refresh_token')
    const savedUser = localStorage.getItem('user')

    if (!token) {
      set({ isLoggedIn: false, isLoading: false })
      return
    }

    // If we have a saved user, restore it immediately
    if (savedUser) {
      try {
        const user = JSON.parse(savedUser)
        set({
          user,
          token,
          refreshToken,
          isLoggedIn: true,
          isLoading: false,
          userAvatar: user.avatar_url || null,
          userType: user.user_type,
          isEnseignant: user.user_type === 'enseignant',
          isChefDept: user.user_type === 'chef_dept',
          isResponsableService: user.user_type === 'responsable_service',
        })
        return
      } catch (err) {
        set({ isLoggedIn: false, isLoading: false })
        localStorage.removeItem('user')
        return
      }
    }

    // If no saved user, just proceed with token
    set({ isLoggedIn: !!token, isLoading: false })
  },

  refreshAuthToken: async () => {
    const state = get()
    if (!state.refreshToken) {
      return false
    }

    try {
      const response = await authService.refreshToken(state.refreshToken)
      if (response.status === 'success' && response.data) {
        localStorage.setItem('access_token', response.data.access_token)
        if (response.data.refresh_token) {
          localStorage.setItem('refresh_token', response.data.refresh_token)
        }

        set({
          token: response.data.access_token,
          refreshToken: response.data.refresh_token || state.refreshToken,
        })
        return true
      }
      return false
    } catch {
      set({ isLoggedIn: false })
      return false
    }
  },

  updateProfile: async (data: Partial<User>) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authService.updateProfile(data)
      if (response.status === 'success' && response.data) {
        set({
          user: response.data,
          isLoading: false,
          userAvatar: response.data.avatar_url || null,
        })
        return true
      } else {
        set({ error: response.message, isLoading: false })
        return false
      }
    } catch (err: any) {
      const message = err.response?.data?.message || 'Failed to update profile'
      set({ error: message, isLoading: false })
      return false
    }
  },

  clearError: () => set({ error: null }),

  uploadAvatar: async (file: File) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authService.uploadAvatar(file)
      if (response.status === 'success' && response.data) {
        const state = get()
        set({
          user: state.user ? { ...state.user, avatar_url: response.data.avatar_url } : null,
          userAvatar: response.data.avatar_url,
          isLoading: false,
        })
        return true
      } else {
        set({ error: response.message, isLoading: false })
        return false
      }
    } catch (err: any) {
      const message = err.response?.data?.message || 'Failed to upload avatar'
      set({ error: message, isLoading: false })
      return false
    }
  },
}))

