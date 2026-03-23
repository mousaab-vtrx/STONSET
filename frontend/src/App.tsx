import React, { useEffect } from 'react'
import { RouterConfig } from '@/router'
import { GlobalToast } from '@/components/shared/GlobalToast'
import { useAuthStore } from '@/store/authStore'

const App: React.FC = () => {
  useEffect(() => {
    // Restore session on app load
    useAuthStore.getState().restoreSession().catch((err) => console.error('Session restore error:', err))
  }, [])

  return (
    <>
      <RouterConfig />
      <GlobalToast />
    </>
  )
}

export default App
