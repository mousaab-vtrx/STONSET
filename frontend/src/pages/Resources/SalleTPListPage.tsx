import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Edit2, Trash2, Eye, Wifi, Projector, Users } from 'lucide-react'
import { PageHeader, Loading, ErrorAlert } from '@/components/shared'
import { useLookups } from '@/hooks/useLookups'
import { useAuth } from '@/hooks/useAuth'

export const SalleTPListPage: React.FC = () => {
  const navigate = useNavigate()
  const { user } = useAuth()
  const { salles, isLoading, error, clearError, fetchSalles } = useLookups()
  const [filteredSalles, setFilteredSalles] = useState<typeof salles>([])
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchSalles()
  }, [])

  useEffect(() => {
    if (searchTerm) {
      setFilteredSalles(
        salles.filter(
          (s) =>
            s.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
            s.location?.toLowerCase().includes(searchTerm.toLowerCase())
        )
      )
    } else {
      setFilteredSalles(salles)
    }
  }, [salles, searchTerm])

  const isServiceManager = user?.user_type === 'responsable_service'

  if (isLoading && salles.length === 0) {
    return <Loading message="Loading TP rooms..." />
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <PageHeader
          title="TP Rooms (Salles TP)"
          description="Manage laboratory and practical work rooms"
        />
        {isServiceManager && (
          <button
            onClick={() => navigate('/salles/new')}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            <span>Add Room</span>
          </button>
        )}
      </div>

      {error && <ErrorAlert message={error} onDismiss={clearError} />}

      {/* Search Bar */}
      <div className="bg-white rounded-lg shadow p-4">
        <input
          type="text"
          placeholder="Search rooms by code or location..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Rooms Grid */}
      {filteredSalles.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <p className="text-gray-500">
            {searchTerm ? 'No rooms match your search' : 'No TP rooms available'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSalles.map((salle) => (
            <div key={salle.id} className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">{salle.code}</h3>
                  <p className="text-sm text-gray-600">{salle.location}</p>
                </div>
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                  {salle.capacite} seats
                </span>
              </div>

              {/* Equipment Indicators */}
              <div className="flex gap-2 mb-6">
                <div title="Internet availability">
                  <Wifi className="w-4 h-4 text-gray-400" />
                </div>
                <div title="Projector availability">
                  <Projector className="w-4 h-4 text-gray-400" />
                </div>
                <div title="Room capacity">
                  <Users className="w-4 h-4 text-gray-400" />
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-2">
                <button
                  onClick={() => navigate(`/salles/${salle.id}`)}
                  className="flex-1 flex items-center justify-center gap-1 px-3 py-2 text-sm bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition-colors"
                >
                  <Eye className="w-4 h-4" />
                  <span>View</span>
                </button>
                {isServiceManager && (
                  <>
                    <button
                      onClick={() => navigate(`/salles/${salle.id}/edit`)}
                      className="flex-1 flex items-center justify-center gap-1 px-3 py-2 text-sm bg-green-50 text-green-600 rounded hover:bg-green-100 transition-colors"
                    >
                      <Edit2 className="w-4 h-4" />
                      <span>Edit</span>
                    </button>
                    <button
                      onClick={() => {
                        if (confirm('Delete this room?')) {
                          // Handle delete
                        }
                      }}
                      className="flex-1 flex items-center justify-center gap-1 px-3 py-2 text-sm bg-red-50 text-red-600 rounded hover:bg-red-100 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                      <span>Delete</span>
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
