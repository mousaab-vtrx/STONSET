import React from 'react'

interface CardProps {
  children: React.ReactNode
  className?: string
  hoverable?: boolean
  elevated?: boolean
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  hoverable = false,
  elevated = false,
}) => {
  const baseClass = elevated ? 'card-elevated' : hoverable ? 'card-hover' : 'card'
  return <div className={`${baseClass} ${className}`}>{children}</div>
}

interface CardHeaderProps {
  title: string
  subtitle?: string
  action?: React.ReactNode
}

export const CardHeader: React.FC<CardHeaderProps> = ({ title, subtitle, action }) => (
  <div className="flex items-start justify-between mb-4 pb-4 border-b border-gray-100">
    <div>
      <h3 className="heading-4">{title}</h3>
      {subtitle && <p className="text-muted text-sm mt-1">{subtitle}</p>}
    </div>
    {action && <div>{action}</div>}
  </div>
)

export const CardBody: React.FC<{ children: React.ReactNode; className?: string }> = ({
  children,
  className = '',
}) => <div className={`space-y-4 ${className}`}>{children}</div>

export const CardFooter: React.FC<{ children: React.ReactNode; className?: string }> = ({
  children,
  className = '',
}) => (
  <div className={`pt-4 border-t border-gray-100 flex items-center justify-between gap-3 ${className}`}>
    {children}
  </div>
)
