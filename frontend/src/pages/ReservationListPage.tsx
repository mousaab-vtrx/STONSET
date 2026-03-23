import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { PageHeader, Loading, ErrorAlert } from '@/components/shared'
import { useReservation } from '@/hooks/useReservation'

export const ReservationListPage: React.FC = () => {
  const { reservations, isLoading, error, fetchReservations, clearError } = useReservation()

  useEffect(() => {
    fetchReservations(0, 100)
  }, [])

  if (isLoading && reservations.length === 0) {
    return <Loading message="Loading reservations..." />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Reservations"
        description="View and manage all your room reservations"
        actions={
          <Link
            to="/reservations/new"
            className="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            New Reservation
          </Link>
        }
      />

      {error && <ErrorAlert message={error} onDismiss={clearError} />}

      {/* Reservations List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {reservations.length === 0 ? (
          <div className="px-6 py-12 text-center">
            <p className="text-gray-500 mb-4">You don't have any reservations yet.</p>
            <Link
              to="/reservations/new"
              className="inline-block px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Create Your First Reservation
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">ID</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Room</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                    Session Date
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Status</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {reservations.map((reservation) => (
                  <tr key={reservation.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">
                      #{reservation.id}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      Room {reservation.salle_tp_id}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {new Date(reservation.date_seance).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {reservation.type_reservation}
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
                        {reservation.etat_id === 2 ? 'Approved' : reservation.etat_id === 3 ? 'Rejected' : 'Pending'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm space-x-2">
                      <Link
                        to={`/reservations/${reservation.id}`}
                        className="text-blue-600 hover:underline"
                      >
                        View
                      </Link>
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
