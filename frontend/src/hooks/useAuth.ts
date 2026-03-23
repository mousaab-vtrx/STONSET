import { useAuthStore } from '@/store/authStore'

export const useAuth = () => {
  // Use a single selector that observes all auth state to ensure proper re-renders
  const authState = useAuthStore((state) => ({
    user: state.user,
    token: state.token,
    refreshToken: state.refreshToken,
    isLoading: state.isLoading,
    error: state.error,
    isLoggedIn: state.isLoggedIn,
    userAvatar: state.userAvatar,
    userType: state.userType,
    isEnseignant: state.isEnseignant,
    isChefDept: state.isChefDept,
    isResponsableService: state.isResponsableService,
    login: state.login,
    register: state.register,
    logout: state.logout,
    updateProfile: state.updateProfile,
    uploadAvatar: state.uploadAvatar,
    clearError: state.clearError,
    checkAuth: state.checkAuth,
    restoreSession: state.restoreSession,
    refreshAuthToken: state.refreshAuthToken,
  }))

  return authState
}
