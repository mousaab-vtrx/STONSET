import React from 'react'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  className = '',
  ...props
}) => (
  <div className="w-full">
    {label && <label className="label-base">{label}</label>}
    <input className={`input-base ${error ? 'border-red-500 focus:ring-red-500' : ''} ${className}`} {...props} />
    {error && <p className="text-red-600 text-xs mt-1">{error}</p>}
    {helperText && !error && <p className="text-gray-500 text-xs mt-1">{helperText}</p>}
  </div>
)

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  rows?: number
}

export const Textarea: React.FC<TextareaProps> = ({ label, error, rows = 4, className = '', ...props }) => (
  <div className="w-full">
    {label && <label className="label-base">{label}</label>}
    <textarea
      rows={rows}
      className={`textarea-base ${error ? 'border-red-500 focus:ring-red-500' : ''} ${className}`}
      {...props}
    />
    {error && <p className="text-red-600 text-xs mt-1">{error}</p>}
  </div>
)

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  options: { value: string | number; label: string }[]
}

export const Select: React.FC<SelectProps> = ({ label, error, options, className = '', ...props }) => (
  <div className="w-full">
    {label && <label className="label-base">{label}</label>}
    <select
      className={`input-base ${error ? 'border-red-500 focus:ring-red-500' : ''} ${className}`}
      {...props}
    >
      <option value="">Select an option...</option>
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
    {error && <p className="text-red-600 text-xs mt-1">{error}</p>}
  </div>
)

interface FormGroupProps {
  children: React.ReactNode
  className?: string
}

export const FormGroup: React.FC<FormGroupProps> = ({ children, className = '' }) => (
  <div className={`space-y-4 ${className}`}>{children}</div>
)

interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
}

export const Checkbox: React.FC<CheckboxProps> = ({ label, ...props }) => (
  <label className="flex items-center gap-2 cursor-pointer">
    <input type="checkbox" className="w-4 h-4 rounded cursor-pointer" {...props} />
    {label && <span className="text-sm">{label}</span>}
  </label>
)
