import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { PageHeader, Loading, ErrorAlert } from '@/components/shared'
import { useAuth } from '@/hooks/useAuth'
import { useReservation } from '@/hooks/useReservation'

interface DashboardStats {
  total: number
  pending: number
  approved: number
  rejected: number
}

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate()
  const { user, userType, isEnseignant, isChefDept, isResponsableService } = useAuth()
  const { reservations, isLoading, error, fetchReservations, clearError } = useReservation()
  const [stats, setStats] = useState<DashboardStats>({
    total: 0,
    pending: 0,
    approved: 0,
    rejected: 0,
  })
  const [isLoadingStats, setIsLoadingStats] = useState(true)
  const [statsError, setStatsError] = useState<string | null>(null)

  useEffect(() => {
    fetchReservations(0, 100)
  }, [])

  useEffect(() => {
    // Calculate statistics from reservations
    if (!isLoading) {
      const newStats = {
        total: reservations.length,
        pending: reservations.filter((r) => r.etat_id === 1).length,
        approved: reservations.filter((r) => r.etat_id === 2).length,
        rejected: reservations.filter((r) => r.etat_id === 3).length,
      }
      setStats(newStats)
      setIsLoadingStats(false)
    }
  }, [reservations, isLoading])

  const retryLoadStats = () => {
    setIsLoadingStats(true)
    setStatsError(null)
    fetchReservations(0, 100)
  }

  const formatUserType = (type: string | null): string => {
    if (!type) return 'Unknown'
    switch (type) {
      case 'enseignant':
        return 'Teacher/Instructor'
      case 'chef_dept':
        return 'Department Head'
      case 'responsable_service':
        return 'Service Manager'
      default:
        return 'User'
    }
  }

  if (isLoading && reservations.length === 0) {
    return <Loading message="Loading your dashboard..." />
  }

  return (
    <div className="space-y-8">
      <PageHeader
        title="Your Dashboard"
        description="Manage and track your room reservations"
      />

      {error && <ErrorAlert message={error} onDismiss={clearError} />}

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-max">
        {/* User Profile Card */}
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
          <h3 className="text-sm font-medium text-gray-600 uppercase mb-4">User Profile</h3>
          <div className="space-y-4">
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {user?.prenom_user} {user?.nom_user}
              </p>
              <p className="text-sm text-gray-600">{user?.email}</p>
            </div>
            <div>
              <span className="text-xs font-semibold text-gray-600 uppercase block mb-1">
                User Type
              </span>
              <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">
                {formatUserType(userType)}
              </span>
            </div>
            <div>
              <span className="text-xs font-semibold text-gray-600 uppercase block mb-1">
                Status
              </span>
              <span
                className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                  user?.is_active
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}
              >
                {user?.is_active ? '✓ Active' : '✗ Inactive'}
              </span>
            </div>
          </div>
        </div>

        {/* Quick Stats Card */}
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg shadow p-6 text-white md:col-span-2">
          <h3 className="text-lg font-bold mb-6">Quick Statistics</h3>
          {isLoadingStats ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
            </div>
          ) : statsError ? (
            <div className="flex flex-col items-center justify-center py-8 space-y-3">
              <svg
                className="w-12 h-12 text-white opacity-70"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
              <p className="text-sm text-white opacity-90 text-center">Unable to load statistics</p>
              <button
                onClick={retryLoadStats}
                className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-sm font-semibold text-white transition-colors"
              >
                Try Again
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-3 gap-4">
              <div className="pb-4 border-b border-white border-opacity-30">
                <span className="text-xs text-white text-opacity-90 block mb-1">Total</span>
                <span className="text-3xl font-bold text-white">{stats.total}</span>
              </div>
              <div className="pb-4 border-b border-white border-opacity-30">
                <span className="text-xs text-white text-opacity-90 block mb-1">Pending</span>
                <span className="text-3xl font-bold text-yellow-200">{stats.pending}</span>
              </div>
              <div className="pb-4 border-b border-white border-opacity-30">
                <span className="text-xs text-white text-opacity-90 block mb-1">Approved</span>
                <span className="text-3xl font-bold text-green-200">{stats.approved}</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions Card */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-900">Quick Actions</h3>
        <div className="flex flex-col sm:flex-row gap-3">
          <button
            onClick={() => navigate('/reservations/new')}
            className="flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            <span>New Reservation</span>
          </button>
          <button
            onClick={() => navigate('/reservations')}
            className="flex items-center justify-center gap-2 px-6 py-3 border-2 border-blue-600 text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 012-2h2a2 2 0 012 2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            <span>View All Reservations</span>
          </button>
        </div>
      </div>

      {/* Information Section */}
      <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
        <div className="flex gap-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            className="w-5 h-5 sm:w-6 sm:h-6 flex-shrink-0 mt-0.5 text-blue-600"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          <div className="text-sm text-gray-700">
            <p className="font-semibold text-gray-900 mb-2">Welcome to your Dashboard!</p>
            <p>
              {isEnseignant &&
                "As a teacher, you can create and manage room reservations for your classes."}
              {isChefDept &&
                "As a department head, you can review and approve reservations from your department's teachers."}
              {isResponsableService &&
                "As a service manager, you can view pending reservations and approve or reject them."}
            </p>
          </div>
        </div>
      </div>

      {/* Recent Reservations */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Recent Reservations</h2>
        </div>
        {reservations.length === 0 ? (
          <div className="px-6 py-12 text-center">
            <p className="text-gray-500">No reservations yet. Start by creating a new one!</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Room</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Date</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Status</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {reservations.slice(0, 5).map((reservation) => (
                  <tr key={reservation.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-900">Room {reservation.salle_tp_id}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {new Date(reservation.date_seance).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          reservation.etat_id === 2
                            ? 'bg-green-100 text-green-800'
                            : reservation.etat_id === 3
                              ? 'bg-red-100 text-red-800'
                              : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {reservation.etat_id === 2
                          ? 'Approved'
                          : reservation.etat_id === 3
                            ? 'Rejected'
                            : 'Pending'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <button
                        onClick={() => navigate(`/reservations/${reservation.id}`)}
                        className="text-blue-600 hover:underline font-medium"
                      >
                        View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
