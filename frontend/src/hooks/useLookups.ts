import { useState, useCallback } from 'react'
import apiClient from '@/services/apiClient'

export interface Creneau {
  id: number
  jour: number
  heure_debut: string
  heure_fin: string
  created_at?: string
  updated_at?: string
}

export interface Module {
  id: number
  code: string
  name: string
  enseignant_id: number
  created_at?: string
  updated_at?: string
}

export interface Section {
  id: number
  code: string
  name: string
  module_id: number
  niveau_id: number
  created_at?: string
  updated_at?: string
}

export interface GroupeTP {
  id: number
  code: string
  effectif: number
  type?: string  // Optional: CM, TD, TP, EXAM, SEMINAR (defaults to TP)
  section_id: number
  created_at?: string
  updated_at?: string
}

export interface Etat {
  id: number
  name: string
  description?: string
  created_at?: string
  updated_at?: string
}

export interface SalleTP {
  id: number
  code: string
  capacite: number
  location?: string
  created_at?: string
  updated_at?: string
}

interface ApiResponse<T> {
  status: string
  data: T
  message: string
  errors: Record<string, any> | null
  meta: Record<string, any> | null
}

export const useLookups = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [creneaux, setCreneaux] = useState<Creneau[]>([])
  const [modules, setModules] = useState<Module[]>([])
  const [sections, setSections] = useState<Section[]>([])
  const [groupesTp, setGroupesTp] = useState<GroupeTP[]>([])
  const [etats, setEtats] = useState<Etat[]>([])
  const [salles, setSalles] = useState<SalleTP[]>([])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  const handleError = (err: any) => {
    const message = err?.message || 'An error occurred'
    setError(message)
    console.error('Lookup Error:', err)
  }

  const fetchCreneaux = useCallback(async (salleId?: number, day?: number) => {
    setIsLoading(true)
    clearError()
    try {
      let url = '/api/v1/creneaux'
      const params: Record<string, any> = {}

      if (day !== undefined) {
        url = `/api/v1/creneaux/day/${day}`
      }
      if (salleId) {
        params.salle_id = salleId
      }

      const response = await apiClient.get<ApiResponse<Creneau[]>>(url, { params })
      const data = response.data

      if (data.status === 'success' && data.data) {
        setCreneaux(data.data)
        console.log('✓ Creneaux loaded:', data.data.length)
      } else {
        setError(data.message || 'Failed to load time slots')
      }
    } catch (err) {
      handleError(err)
    } finally {
      setIsLoading(false)
    }
  }, [clearError])

  const fetchModules = useCallback(async () => {
    setIsLoading(true)
    clearError()
    try {
      console.log('[useLookups] Fetching modules from /api/v1/modules')
      const response = await apiClient.get<ApiResponse<Module[]>>('/api/v1/modules')
      const data = response.data

      console.log('[useLookups] API Response:', data)

      if (data.status === 'success' && data.data && Array.isArray(data.data)) {
        setModules(data.data)
        console.log('[useLookups] Modules loaded successfully:', data.data.length, 'items')
      } else {
        console.warn('[useLookups] Unexpected modules response:', data)
        setError('Failed to load modules: Invalid response format')
      }
    } catch (err) {
      console.error('[useLookups] Error fetching modules:', err)
      handleError(err)
    } finally {
      setIsLoading(false)
    }
  }, [clearError])

  const fetchSectionsByModule = useCallback(async (moduleId: number) => {
    setIsLoading(true)
    clearError()
    try {
      const response = await apiClient.get<ApiResponse<Section[]>>(
        `/api/v1/sections/module/${moduleId}`
      )
      const data = response.data

      if (data.status === 'success' && data.data) {
        setSections(data.data)
      } else {
        setError(data.message || 'Failed to load sections')
      }
    } catch (err) {
      handleError(err)
    } finally {
      setIsLoading(false)
    }
  }, [clearError])

  const fetchGroupesTpBySection = useCallback(async (sectionId: number) => {
    setIsLoading(true)
    clearError()
    try {
      const response = await apiClient.get<ApiResponse<GroupeTP[]>>(
        `/api/v1/groupes/section/${sectionId}`
      )
      const data = response.data

      if (data.status === 'success' && data.data) {
        setGroupesTp(data.data)
      } else {
        setError(data.message || 'Failed to load groups')
      }
    } catch (err) {
      handleError(err)
    } finally {
      setIsLoading(false)
    }
  }, [clearError])

  const fetchEtats = useCallback(async () => {
    setIsLoading(true)
    clearError()
    try {
      const response = await apiClient.get<ApiResponse<Etat[]>>('/api/v1/etats')
      const data = response.data

      if (data.status === 'success' && data.data) {
        setEtats(data.data)
        console.log('✓ Etats loaded:', data.data.length)
      } else {
        setError(data.message || 'Failed to load statuses')
      }
    } catch (err) {
      handleError(err)
    } finally {
      setIsLoading(false)
    }
  }, [clearError])

  const fetchSalles = useCallback(async () => {
    setIsLoading(true)
    clearError()
    try {
      const response = await apiClient.get<ApiResponse<SalleTP[]>>('/api/v1/salles-tp')
      const data = response.data

      if (data.status === 'success' && data.data) {
        setSalles(data.data)
        console.log('✓ Salles loaded:', data.data.length)
      } else {
        setError(data.message || 'Failed to load rooms')
      }
    } catch (err) {
      handleError(err)
    } finally {
      setIsLoading(false)
    }
  }, [clearError])

  return {
    isLoading,
    error,
    creneaux,
    modules,
    sections,
    groupesTp,
    etats,
    salles,
    clearError,
    fetchCreneaux,
    fetchModules,
    fetchSectionsByModule,
    fetchGroupesTpBySection,
    fetchEtats,
    fetchSalles,
  }
}
