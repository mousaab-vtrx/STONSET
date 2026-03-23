import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Calendar,
  Clock,
  MapPin,
  Users,
  BookOpen,
  Wifi,
  Monitor,
  Save,
  X,
} from 'lucide-react'
import { PageHeader, ErrorAlert } from '@/components/shared'
import { useReservation } from '@/hooks/useReservation'
import { useLookups } from '@/hooks/useLookups'
import { useAuth } from '@/hooks/useAuth'
import type { ReservationCreate } from '@/types'

export const ReservationCreatePage: React.FC = () => {
  const navigate = useNavigate()
  const authData = useAuth()
  const reservationData = useReservation()
  const lookupsData = useLookups()

  // Ensure defaults
  const user = authData?.user
  const createReservation = reservationData?.createReservation
  const isLoading = reservationData?.isLoading || false
  const salles = lookupsData?.salles || []
  const creneaux = lookupsData?.creneaux || []
  const groupesTp = lookupsData?.groupesTp || []
  const fetchSalles = lookupsData?.fetchSalles
  const fetchCreneaux = lookupsData?.fetchCreneaux

  const enseignantId = user?.id || 1

  const [formData, setFormData] = useState<ReservationCreate>({
    date_seance: '',
    salle_tp_id: 0,
    creneau_id: 0,
    groupe_tp_id: 0,
    enseignant_id: enseignantId,
    etat_id: 1,
    access_internet: false,
    equipement_reseau: false,
    videoprojecteur: false,
    type_reservation: 'TP',
    notes: '',
  })

  const [error, setError] = useState<string | null>(null)
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    const loadData = async () => {
      try {
        if (fetchSalles) await fetchSalles()
        if (fetchCreneaux) await fetchCreneaux()
      } catch (err) {
        // Silently handle error - user sees message if data fails to load
      }
    }
    loadData()
  }, [])

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {}

    if (!formData.date_seance) {
      errors.date_seance = 'Session date is required'
    }

    if (!formData.salle_tp_id || formData.salle_tp_id === 0) {
      errors.salle_tp_id = 'Please select a room'
    }

    if (!formData.creneau_id || formData.creneau_id === 0) {
      errors.creneau_id = 'Please select a time slot'
    }

    if (!formData.groupe_tp_id || formData.groupe_tp_id === 0) {
      errors.groupe_tp_id = 'Please select a group TP'
    }

    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (!validateForm()) {
      setError('Please fill in all required fields')
      return
    }

    try {
      if (!createReservation) {
        throw new Error('Create reservation function not available')
      }
      const success = await createReservation(formData)
      if (success) {
        navigate('/reservations')
      } else {
        setError('Failed to create reservation')
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred')
    }
  }

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target
    const fieldValue = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value

    setFormData((prev) => ({
      ...prev,
      [name]: fieldValue,
    }))

    if (validationErrors[name]) {
      setValidationErrors((prev) => {
        const newErrors = { ...prev }
        delete newErrors[name]
        return newErrors
      })
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 py-8 transition-colors duration-200">
      <div className="max-w-4xl mx-auto">
        <PageHeader
          title="Create New Reservation"
          description="Reserve a lab room for your session"
        />

        {error && (
          <ErrorAlert
            message={error}
            onDismiss={() => setError(null)}
          />
        )}

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mt-6">
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Basic Information */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <Calendar size={20} className="text-blue-500" />
                Basic Information
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <Calendar size={18} className="inline mr-2 text-blue-500" />
                    Session Date *
                  </label>
                  <input
                    type="date"
                    name="date_seance"
                    value={formData.date_seance}
                    onChange={handleChange}
                    className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      validationErrors.date_seance ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                    }`}
                  />
                  {validationErrors.date_seance && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.date_seance}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <BookOpen size={18} className="inline mr-2 text-blue-500" />
                    Reservation Type *
                  </label>
                  <select
                    name="type_reservation"
                    value={formData.type_reservation}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="TP">Practical Work (TP)</option>
                    <option value="EXAM">Exam</option>
                    <option value="SEMINAR">Seminar</option>
                    <option value="WORKSHOP">Workshop</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Room & Scheduling */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <MapPin size={20} className="text-blue-500" />
                Room & Scheduling
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <MapPin size={18} className="inline mr-2 text-blue-500" />
                    Lab Room *
                  </label>
                  <select
                    name="salle_tp_id"
                    value={formData.salle_tp_id}
                    onChange={handleChange}
                    className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      validationErrors.salle_tp_id ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                    }`}
                  >
                    <option value={0}>Select Room</option>
                    {salles.map((salle) => (
                      <option key={salle.id} value={salle.id}>
                        {salle.code} (Capacity: {salle.capacite})
                      </option>
                    ))}
                  </select>
                  {validationErrors.salle_tp_id && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.salle_tp_id}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <Clock size={18} className="inline mr-2 text-blue-500" />
                    Time Slot *
                  </label>
                  <select
                    name="creneau_id"
                    value={formData.creneau_id}
                    onChange={handleChange}
                    className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      validationErrors.creneau_id ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                    }`}
                  >
                    <option value={0}>Select Time Slot</option>
                    {creneaux.map((creneau) => (
                      <option key={creneau.id} value={creneau.id}>
                        {creneau.heure_debut} - {creneau.heure_fin}
                      </option>
                    ))}
                  </select>
                  {validationErrors.creneau_id && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.creneau_id}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <Users size={18} className="inline mr-2 text-blue-500" />
                    Group TP *
                  </label>
                  <select
                    name="groupe_tp_id"
                    value={formData.groupe_tp_id}
                    onChange={handleChange}
                    className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      validationErrors.groupe_tp_id ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                    }`}
                  >
                    <option value={0}>Select Group</option>
                    {groupesTp.map((groupe) => (
                      <option key={groupe.id} value={groupe.id}>
                        {groupe.code}
                      </option>
                    ))}
                  </select>
                  {validationErrors.groupe_tp_id && (
                    <p className="text-red-500 text-sm mt-1">{validationErrors.groupe_tp_id}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Equipment & Resources */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <Monitor size={20} className="text-blue-500" />
                Equipment & Resources
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <label className="flex items-center p-4 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer transition-colors">
                  <input
                    type="checkbox"
                    name="access_internet"
                    checked={formData.access_internet}
                    onChange={handleChange}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <div className="ml-3 flex items-center gap-2">
                    <Wifi size={18} className="text-blue-500" />
                    <span className="font-medium text-gray-700 dark:text-gray-300">Internet Access</span>
                  </div>
                </label>

                <label className="flex items-center p-4 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer transition-colors">
                  <input
                    type="checkbox"
                    name="equipement_reseau"
                    checked={formData.equipement_reseau}
                    onChange={handleChange}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <div className="ml-3 flex items-center gap-2">
                    <Monitor size={18} className="text-blue-500" />
                    <span className="font-medium text-gray-700 dark:text-gray-300">Network Equipment</span>
                  </div>
                </label>

                <label className="flex items-center p-4 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer transition-colors">
                  <input
                    type="checkbox"
                    name="videoprojecteur"
                    checked={formData.videoprojecteur}
                    onChange={handleChange}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <div className="ml-3 flex items-center gap-2">
                    <Monitor size={18} className="text-blue-500" />
                    <span className="font-medium text-gray-700 dark:text-gray-300">Video Projector</span>
                  </div>
                </label>
              </div>
            </div>

            {/* Additional Notes */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Additional Notes</h3>
              <textarea
                name="notes"
                placeholder="Add any special requests or notes..."
                value={formData.notes || ''}
                onChange={handleChange}
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Form Actions */}
            <div className="border-t border-gray-200 dark:border-gray-600 pt-6 flex justify-between gap-3">
              <button
                type="button"
                onClick={() => navigate('/reservations')}
                className="inline-flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-medium rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              >
                <X size={18} />
                Cancel
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="inline-flex items-center gap-2 px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400"
              >
                <Save size={18} />
                {isLoading ? 'Creating...' : 'Create Reservation'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
