import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Edit2, Trash2, Eye } from 'lucide-react'
import { PageHeader, Loading, ErrorAlert } from '@/components/shared'
import { useLookups } from '@/hooks/useLookups'
import { useAuth } from '@/hooks/useAuth'

export const ModuleListPage: React.FC = () => {
  const navigate = useNavigate()
  const { user } = useAuth()
  const { modules, isLoading, error, clearError, fetchModules } = useLookups()
  const [filteredModules, setFilteredModules] = useState<typeof modules>([])
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchModules()
  }, [])

  useEffect(() => {
    if (searchTerm) {
      setFilteredModules(
        modules.filter(
          (m) =>
            m.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            m.code.toLowerCase().includes(searchTerm.toLowerCase())
        )
      )
    } else {
      setFilteredModules(modules)
    }
  }, [modules, searchTerm])

  const isServiceManager = user?.user_type === 'responsable_service'

  if (isLoading && modules.length === 0) {
    return <Loading message="Loading modules..." />
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <PageHeader title="Modules" description="Manage course modules available in the system" />
        {isServiceManager && (
          <button
            onClick={() => navigate('/modules/new')}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            <span>Add Module</span>
          </button>
        )}
      </div>

      {error && <ErrorAlert message={error} onDismiss={clearError} />}

      {/* Search Bar */}
      <div className="bg-white rounded-lg shadow p-4">
        <input
          type="text"
          placeholder="Search modules by name or code..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Modules Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Code</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Name</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                  Instructor
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                  Sections
                </th>
                <th className="px-6 py-3 text-right text-sm font-semibold text-gray-900">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredModules.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                    {searchTerm ? 'No modules match your search' : 'No modules available'}
                  </td>
                </tr>
              ) : (
                filteredModules.map((module) => (
                  <tr key={module.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">{module.code}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{module.name}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">Instructor {module.enseignant_id}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">-</td>
                    <td className="px-6 py-4 text-right space-x-2">
                      <button
                        onClick={() => navigate(`/modules/${module.id}`)}
                        className="text-blue-600 hover:text-blue-800 p-1"
                        title="View details"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      {isServiceManager && (
                        <>
                          <button
                            onClick={() => navigate(`/modules/${module.id}/edit`)}
                            className="text-green-600 hover:text-green-800 p-1"
                            title="Edit"
                          >
                            <Edit2 className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => {
                              if (confirm('Delete this module?')) {
                                // Handle delete
                              }
                            }}
                            className="text-red-600 hover:text-red-800 p-1"
                            title="Delete"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
