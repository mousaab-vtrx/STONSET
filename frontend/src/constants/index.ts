/**
 * Application Constants
 */

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export const API_PREFIX = '/api/v1'
export const API_TIMEOUT = 30000 // 30 seconds

// Authentication
export const AUTH_TOKEN_KEY = 'access_token'
export const REFRESH_TOKEN_KEY = 'refresh_token'
export const USER_KEY = 'user'
export const TOKEN_HEADER = 'Authorization'

// User Types
export const USER_TYPES = {
  ENSEIGNANT: 'enseignant',
  CHEF_DEPT: 'chef_dept',
  RESPONSABLE_SERVICE: 'responsable_service',
  ADMIN: 'admin',
} as const

// Reservation Status
export const RESERVATION_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  CANCELLED: 'cancelled',
} as const

// UI Configuration
export const TOAST_DURATION = 5000 // 5 seconds
export const DEBOUNCE_DELAY = 300 // milliseconds
export const ANIMATION_DURATION = 200 // milliseconds

// Pagination
export const ITEMS_PER_PAGE = 10
export const MAX_ITEMS_PER_PAGE = 100

// File Upload
export const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5 MB
export const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']

// Date Formats
export const DATE_FORMAT = 'PPP' // "Jan 1, 2023"
export const DATETIME_FORMAT = 'PPp' // "Jan 1, 2023, 1:00 PM"
export const TIME_FORMAT = 'HH:mm' // "13:00"

// Validation Rules
export const VALIDATION = {
  PASSWORD_MIN_LENGTH: 8,
  EMAIL_REGEX: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE_REGEX: /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/,
} as const

// Feature Flags
export const FEATURES = {
  ENABLE_DARK_MODE: true,
  ENABLE_NOTIFICATIONS: true,
  ENABLE_ANALYTICS: false,
  ENABLE_DEBUG_MODE: false,
} as const

// Routes
export const ROUTES = {
  ROOT: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  RESERVATIONS: '/reservations',
  RESERVATIONS_NEW: '/reservations/new',
  RESERVATION_DETAIL: (id: number) => `/reservations/${id}`,
  PROFILE: '/profile',
  SETTINGS: '/settings',
  PRIVACY: '/privacy-policy',
  TERMS: '/terms-of-service',
  COOKIES: '/cookie-policy',
} as const

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  UNAUTHORIZED: 'Your session has expired. Please log in again.',
  FORBIDDEN: 'You do not have permission to access this resource.',
  NOT_FOUND: 'The requested resource was not found.',
  VALIDATION_ERROR: 'Please check the form and try again.',
  SERVER_ERROR: 'An unexpected server error occurred. Please try again later.',
  GENERIC: 'An error occurred. Please try again.',
} as const

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN: 'Logged in successfully!',
  LOGOUT: 'Logged out successfully!',
  REGISTRATION: 'Account created successfully! Welcome to STONSET!',
  PROFILE_UPDATED: 'Profile updated successfully!',
  AVATAR_UPLOADED: 'Avatar updated successfully!',
  RESERVATION_CREATED: 'Reservation created successfully!',
  RESERVATION_UPDATED: 'Reservation updated successfully!',
  RESERVATION_DELETED: 'Reservation deleted successfully!',
} as const

// Color Palette
export const COLORS = {
  PRIMARY: '#3b82f6', // Blue
  PRIMARY_DARK: '#1e40af',
  PRIMARY_LIGHT: '#93c5fd',
  ACCENT: '#8b5cf6', // Purple
  ACCENT_DARK: '#7c3aed',
  ACCENT_LIGHT: '#a78bfa',
  SUCCESS: '#10b981', // Green
  WARNING: '#f59e0b', // Amber
  ERROR: '#ef4444', // Red
  INFO: '#3b82f6', // Blue
  GRAY: '#6b7280',
  GRAY_DARK: '#374151',
  GRAY_LIGHT: '#f3f4f6',
} as const

// API Response Status
export const RESPONSE_STATUS = {
  SUCCESS: 'success',
  ERROR: 'error',
  VALIDATION_ERROR: 'validation_error',
} as const
