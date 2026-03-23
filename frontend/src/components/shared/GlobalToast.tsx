import React, { useEffect } from 'react'
import { CheckCircle, AlertCircle, AlertTriangle, Info, X } from 'lucide-react'
import { useToast } from '@/hooks/useToast'

interface ToastItemProps {
  id: string
  message: string
  type: 'success' | 'error' | 'warning' | 'info'
  onRemove: (id: string) => void
}

const ToastItem: React.FC<ToastItemProps> = ({ id, message, type, onRemove }) => {
  useEffect(() => {
    const timer = setTimeout(() => onRemove(id), 5000)
    return () => clearTimeout(timer)
  }, [id, onRemove])

  const colorClasses = {
    success: 'bg-green-50 text-green-800 border-green-200',
    error: 'bg-red-50 text-red-800 border-red-200',
    warning: 'bg-yellow-50 text-yellow-800 border-yellow-200',
    info: 'bg-blue-50 text-blue-800 border-blue-200',
  }

  const iconClasses = {
    success: 'text-green-400',
    error: 'text-red-400',
    warning: 'text-yellow-400',
    info: 'text-blue-400',
  }

  return (
    <div className={`rounded-lg border p-4 ${colorClasses[type]} flex items-start`}>
      <div className={`flex-shrink-0 ${iconClasses[type]}`}>
        {type === 'success' && <CheckCircle className="h-5 w-5" />}
        {type === 'error' && <AlertCircle className="h-5 w-5" />}
        {type === 'warning' && <AlertTriangle className="h-5 w-5" />}
        {type === 'info' && <Info className="h-5 w-5" />}
      </div>
      <div className="ml-3 flex-1">
        <p className="text-sm font-medium">{message}</p>
      </div>
      <button
        onClick={() => onRemove(id)}
        className="ml-4 inline-flex text-gray-400 hover:text-gray-500"
      >
        <span className="sr-only">Close</span>
        <X className="h-5 w-5" />
      </button>
    </div>
  )
}

export const GlobalToast: React.FC = () => {
  const { toasts, removeToast } = useToast()

  return (
    <div className="fixed bottom-4 right-4 z-50 space-y-3 w-full max-w-sm px-4 sm:px-0">
      {toasts.map((toast) => (
        <ToastItem
          key={toast.id}
          id={toast.id}
          message={toast.message}
          type={toast.type}
          onRemove={removeToast}
        />
      ))}
    </div>
  )
}
