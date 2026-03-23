import React from 'react'
import { AlertCircle, X } from 'lucide-react'

interface ErrorAlertProps {
  message: string
  onDismiss?: () => void
  title?: string
}

export const ErrorAlert: React.FC<ErrorAlertProps> = ({ message, onDismiss, title = 'Error' }) => {
  return (
    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-4">
      <div className="flex">
        <div className="flex-shrink-0">
          <AlertCircle className="h-5 w-5 text-red-400 dark:text-red-400" />
        </div>
        <div className="ml-3">
          <h3 className="text-sm font-medium text-red-800 dark:text-red-300">{title}</h3>
          <p className="mt-2 text-sm text-red-700 dark:text-red-400">{message}</p>
        </div>
        {onDismiss && (
          <div className="ml-auto">
            <button
              onClick={onDismiss}
              className="inline-flex text-gray-400 hover:text-gray-500 dark:hover:text-gray-400 focus:outline-none"
            >
              <span className="sr-only">Dismiss</span>
              <X className="h-5 w-5" />
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
