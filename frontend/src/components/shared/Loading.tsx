import React from 'react'
import { clsx } from '@/utils/helpers'

interface LoadingProps {
  size?: 'sm' | 'md' | 'lg'
  message?: string
  fullScreen?: boolean
}

export const Loading: React.FC<LoadingProps> = ({ size = 'md', message, fullScreen }) => {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  }

  const spinner = (
    <div className={clsx('animate-spin rounded-full border-4 border-gray-300 border-t-primary', sizeClasses[size])}>
    </div>
  )

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-white/80 dark:bg-gray-900/80 z-50">
        <div className="text-center">
          {spinner}
          {message && <p className="mt-4 text-gray-600 dark:text-gray-400">{message}</p>}
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col items-center justify-center py-8">
      {spinner}
      {message && <p className="mt-4 text-gray-600 dark:text-gray-400">{message}</p>}
    </div>
  )
}
