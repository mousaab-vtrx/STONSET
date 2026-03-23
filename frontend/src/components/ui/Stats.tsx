import React from 'react'
import { Users, Calendar, Building2, Check } from 'lucide-react'

const iconMap: Record<string, React.FC<{ className?: string }>> = {
  users: Users,
  calendar: Calendar,
  building: Building2,
  check: Check,
}

interface StatCardProps {
  label: string
  value: string | number
  icon?: string
  change?: { value: number; trend: 'up' | 'down' }
  className?: string
}

export const StatCard: React.FC<StatCardProps> = ({
  label,
  value,
  icon,
  change,
  className = '',
}) => {
  const IconComponent = icon ? iconMap[icon] : null
  return (
    <div className={`card-hover ${className}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-muted text-sm font-medium">{label}</p>
          <p className="heading-3 mt-2">{value}</p>
          {change && (
            <p className={`text-xs mt-2 ${change.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
              {change.trend === 'up' ? '↑' : '↓'} {change.value}%
            </p>
          )}
        </div>
        {IconComponent && <IconComponent className="w-8 h-8 text-gray-400 opacity-75" />}
      </div>
    </div>
  )
}

interface TableProps {
  columns: { key: string; label: string; render?: (value: any, row: any) => React.ReactNode }[]
  data: any[]
  striped?: boolean
}

export const Table: React.FC<TableProps> = ({ columns, data, striped = true }) => (
  <div className="overflow-x-auto">
    <table className="w-full">
      <thead>
        <tr className="border-b border-gray-200 bg-gray-50">
          {columns.map((col) => (
            <th
              key={col.key}
              className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
            >
              {col.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, idx) => (
          <tr
            key={idx}
            className={`border-b border-gray-100 ${
              striped && idx % 2 === 1 ? 'bg-gray-50' : ''
            } hover:bg-gray-50 transition-colors`}
          >
            {columns.map((col) => (
              <td key={col.key} className="px-6 py-4 text-sm">
                {col.render ? col.render(row[col.key], row) : row[col.key]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)

export const EmptyState: React.FC<{ title: string; description?: string; action?: React.ReactNode }> = ({
  title,
  description,
  action,
}) => (
  <div className="text-center py-12 px-4">
    <p className="text-3xl mb-4">📭</p>
    <h3 className="heading-4 mb-2">{title}</h3>
    {description && <p className="text-muted mb-4">{description}</p>}
    {action && <div>{action}</div>}
  </div>
)
