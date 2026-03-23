import { create } from 'zustand'

interface Toast {
  id: string
  message: string
  type: 'success' | 'error' | 'warning' | 'info'
  duration?: number
}

interface ToastState {
  toasts: Toast[]
  addToast: (message: string, type: Toast['type'], duration?: number) => void
  removeToast: (id: string) => void
  clearToasts: () => void
}

const useToastStore = create<ToastState>((set) => ({
  toasts: [],
  addToast: (message: string, type: Toast['type'], duration = 5000) => {
    const id = `${Date.now()}`
    set((state) => ({
      toasts: [...state.toasts, { id, message, type, duration }],
    }))

    if (duration > 0) {
      setTimeout(() => {
        set((state) => ({
          toasts: state.toasts.filter((t) => t.id !== id),
        }))
      }, duration)
    }
  },
  removeToast: (id: string) =>
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    })),
  clearToasts: () => set({ toasts: [] }),
}))

export const useToast = () => {
  const store = useToastStore()

  return {
    toasts: store.toasts,
    success: (message: string) => store.addToast(message, 'success'),
    error: (message: string) => store.addToast(message, 'error'),
    warning: (message: string) => store.addToast(message, 'warning'),
    info: (message: string) => store.addToast(message, 'info'),
    removeToast: store.removeToast,
    clearToasts: store.clearToasts,
  }
}
