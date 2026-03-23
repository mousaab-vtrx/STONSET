import React, { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Calendar,
  Clock,
  MapPin,
  CheckCircle,
  XCircle,
  AlertCircle,
  Wifi,
  Monitor,
  ArrowLeft,
  Users,
  BookOpen,
  ChevronRight,
  Check,
  X,
} from 'lucide-react'
import { PageHeader, Loading, ErrorAlert } from '@/components/shared'
import { useReservation } from '@/hooks/useReservation'

const getStatusBadge = (etat_id: number) => {
  if (etat_id === 2) {
    return { icon: CheckCircle, label: 'Approved', color: 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 border-green-200 dark:border-green-800' }
  }
  if (etat_id === 3) {
    return { icon: XCircle, label: 'Rejected', color: 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 border-red-200 dark:border-red-800' }
  }
  return { icon: AlertCircle, label: 'Pending', color: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-400 border-yellow-200 dark:border-yellow-800' }
}

const InfoField: React.FC<{ icon: React.ReactNode; label: string; value: React.ReactNode }> = ({
  icon,
  label,
  value,
}) => (
  <div className="flex items-start space-x-3">
    <div className="flex-shrink-0 mt-1 text-blue-500">{icon}</div>
    <div className="flex-grow">
      <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{label}</p>
      <p className="text-base font-semibold text-gray-900 dark:text-white mt-1">{value}</p>
    </div>
  </div>
)

const FeatureToggle: React.FC<{ icon: React.ReactNode; label: string; enabled: boolean }> = ({
  icon,
  label,
  enabled,
}) => (
  <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
    <div className="flex items-center space-x-3">
      <div className="text-gray-600 dark:text-gray-400">{icon}</div>
      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{label}</span>
    </div>
    <div className={`flex items-center space-x-1 font-semibold ${enabled ? 'text-green-600 dark:text-green-400' : 'text-gray-400 dark:text-gray-500'}`}>
      {enabled ? <Check size={20} /> : <X size={20} />}
    </div>
  </div>
)

export const ReservationDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { selectedReservation, isLoading, error, fetchReservationById, clearError } = useReservation()

  // Validate and parse ID
  const reservationId = id ? parseInt(id, 10) : null
  const isInvalidId = !id || isNaN(reservationId!) || reservationId! <= 0

  useEffect(() => {
    if (!isInvalidId && reservationId) {
      fetchReservationById(reservationId)
    }
  }, [reservationId, isInvalidId])

  // Show error for invalid ID
  if (isInvalidId) {
    return (
      <div className="space-y-6">
        <PageHeader title="Invalid Reservation" description="The requested reservation could not be found" />
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <ErrorAlert
            message={`Invalid reservation ID: ${id}. Please use a valid numeric ID.`}
            onDismiss={() => navigate('/reservations')}
          />
          <div className="mt-6">
            <button
              onClick={() => navigate('/reservations')}
              className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              <ArrowLeft size={18} />
              <span>Back to Reservations</span>
            </button>
          </div>
        </div>
      </div>
    )
  }

  // Show loading state
  if (isLoading) {
    return <Loading message="Loading reservation details..." />
  }

  // Show error state if fetch failed
  if (error && !selectedReservation) {
    return (
      <div className="space-y-6">
        <PageHeader title="Error Loading Reservation" description="Something went wrong" />
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <ErrorAlert message={error} onDismiss={clearError} />
          <div className="mt-6">
            <button
              onClick={() => navigate('/reservations')}
              className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              <ArrowLeft size={18} />
              <span>Back to Reservations</span>
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (!selectedReservation) {
    return <Loading message="Loading reservation details..." />
  }

  const statusBadge = getStatusBadge(selectedReservation.etat_id)
  const StatusIcon = statusBadge.icon

  const sessionDate = new Date(selectedReservation.date_seance)
  const requestDate = new Date(selectedReservation.date_demande)

  return (
    <div className="space-y-6">
      <PageHeader
        title={`Reservation #${selectedReservation.id}`}
        description="View and manage reservation details"
      />

      {error && <ErrorAlert message={error} onDismiss={clearError} />}

      {/* Status Banner */}
      <div className={`border-l-4 rounded-lg p-4 ${statusBadge.color}`}>
        <div className="flex items-center space-x-3">
          <StatusIcon size={24} />
          <div>
            <h3 className="font-semibold">{statusBadge.label}</h3>
            <p className="text-sm opacity-75">
              {selectedReservation.etat_id === 2 && 'This reservation has been approved'}
              {selectedReservation.etat_id === 3 && 'This reservation has been rejected'}
              {selectedReservation.etat_id === 1 && 'This reservation is awaiting approval'}
            </p>
          </div>
        </div>
      </div>

      {/* Main Details Card */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
        {/* Header with room info */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 px-6 py-8 border-b border-blue-100 dark:border-blue-800/50">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-blue-100 rounded-lg p-3">
                <MapPin className="text-blue-600" size={28} />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Lab Room</p>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-1">Room {selectedReservation.salle_tp_id}</h2>
              </div>
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold text-gray-900 dark:text-white">#{selectedReservation.id}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Reservation ID</p>
            </div>
          </div>
        </div>

        <div className="p-6 space-y-8">
          {/* Session Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
              <Calendar size={20} className="text-blue-500" />
              <span>Session Information</span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InfoField
                icon={<Calendar size={20} />}
                label="Session Date"
                value={sessionDate.toLocaleDateString('en-US', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              />
              <InfoField
                icon={<Clock size={20} />}
                label="Requested On"
                value={requestDate.toLocaleString('en-US', {
                  month: 'short',
                  day: 'numeric',
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              />
            </div>
          </div>

          {/* Reservation Details */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
              <BookOpen size={20} className="text-blue-500" />
              <span>Reservation Details</span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InfoField
                icon={<BookOpen size={20} />}
                label="Reservation Type"
                value={selectedReservation.type_reservation || 'Standard'}
              />
              <InfoField
                icon={<Clock size={20} />}
                label="Time Slot"
                value={`Créneau #${selectedReservation.creneau_id}`}
              />
              <InfoField
                icon={<Users size={20} />}
                label="Group TP"
                value={`Group #${selectedReservation.groupe_tp_id}`}
              />
            </div>
          </div>

          {/* Equipment & Resources */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
              <Monitor size={20} className="text-blue-500" />
              <span>Equipment & Resources</span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <FeatureToggle
                icon={<Wifi size={20} />}
                label="Internet Access"
                enabled={selectedReservation.access_internet}
              />
              <FeatureToggle
                icon={<Monitor size={20} />}
                label="Network Equipment"
                enabled={selectedReservation.equipement_reseau}
              />
              <FeatureToggle
                icon={<Monitor size={20} />}
                label="Video Projector"
                enabled={selectedReservation.videoprojecteur}
              />
            </div>
          </div>

          {/* Notes */}
          {selectedReservation.notes && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Additional Notes</h3>
              <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed">{selectedReservation.notes}</p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 dark:bg-gray-700 px-6 py-4 border-t border-gray-200 dark:border-gray-600 flex justify-between items-center">
          <button
            onClick={() => navigate('/reservations')}
            className="inline-flex items-center space-x-2 px-4 py-2 bg-white dark:bg-gray-600 border border-gray-300 dark:border-gray-500 text-gray-700 dark:text-gray-300 font-medium rounded-lg hover:bg-gray-100 dark:hover:bg-gray-500 transition-colors"
          >
            <ArrowLeft size={18} />
            <span>Back to List</span>
          </button>
          <button
            onClick={() => navigate(`/reservations/${selectedReservation.id}/edit`)}
            className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <span>Edit</span>
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
    </div>
  )
}
