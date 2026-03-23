/**
 * Type definitions for the application
 * Maps to backend models defined in app/models/
 */

// ============ API Response Types ============
export interface ApiResponse<T> {
  status: string
  data: T | null
  message: string
  errors: Record<string, any> | null
  meta: Record<string, any> | null
}

// ============ User & Auth Types ============
export interface User {
  id: number
  email: string
  nom_user: string
  prenom_user: string
  user_type: 'enseignant' | 'chef_dept' | 'responsable_service' | 'admin'
  avatar_url?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  nom_user: string
  prenom_user: string
  user_type?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token?: string
  user: User
}

// ============ Core Domain Types ============
export interface Department {
  id: number
  name: string
  description?: string
  head_id?: number
  created_at: string
  updated_at: string
}

export interface Module {
  id: number
  name: string
  code: string
  description?: string
  department_id: number
  credits?: number
  created_at: string
  updated_at: string
}

export interface Niveau {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface Filiere {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface Section {
  id: number
  name: string
  filiere_id: number
  niveau_id: number
  created_at: string
  updated_at: string
}

export interface GroupeTP {
  id: number
  name: string
  type?: string  // Optional: CM, TD, TP, EXAM, SEMINAR (defaults to TP)
  section_id: number
  created_at: string
  updated_at: string
}

// ============ Room & Equipment Types ============
export interface SalleTP {
  id: number
  name: string
  capacity: number
  location?: string
  department_id?: number
  description?: string
  created_at: string
  updated_at: string
}

export interface Logiciel {
  id: number
  name: string
  version?: string
  license_type?: string
  created_at: string
  updated_at: string
}

export interface Systeme {
  id: number
  name: string
  version?: string
  created_at: string
  updated_at: string
}

// ============ Schedule & Time Types ============
export interface Creneau {
  id: number
  start_time: string
  end_time: string
  day_of_week: number
  created_at: string
  updated_at: string
}

export interface Vacances {
  id: number
  name: string
  start_date: string
  end_date: string
  created_at: string
  updated_at: string
}

export interface Etat {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

// ============ Reservation Types ============
export interface Reservation {
  id: number
  date_seance: string
  date_demande: string
  date_reponse?: string | null
  access_internet: boolean
  equipement_reseau: boolean
  videoprojecteur: boolean
  type_reservation: string
  notes?: string | null
  enseignant_id: number
  salle_tp_id: number
  creneau_id: number
  etat_id: number
  groupe_tp_id: number
  vacances_id?: number | null
  created_at: string
  updated_at: string
}

export interface ReservationCreate {
  date_seance: string
  access_internet?: boolean
  equipement_reseau?: boolean
  videoprojecteur?: boolean
  type_reservation?: string
  notes?: string
  enseignant_id: number
  salle_tp_id: number
  creneau_id: number
  etat_id: number
  groupe_tp_id: number
  vacances_id?: number
}

export interface ReservationUpdate {
  date_seance?: string
  access_internet?: boolean
  equipement_reseau?: boolean
  videoprojecteur?: boolean
  type_reservation?: string
  notes?: string
  etat_id?: number
  vacances_id?: number
}

// ============ Other Types ============
export interface DomainPlaceholder {
  id: number
  name: string
  created_at: string
  updated_at: string
}

export interface AccountDeletionFeedback {
  id: number
  user_id: number
  reason: string
  feedback: string
  created_at: string
  updated_at: string
}
