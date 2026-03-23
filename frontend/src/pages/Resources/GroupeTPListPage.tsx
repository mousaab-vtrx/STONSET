import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Edit2, Trash2, Eye, Users } from 'lucide-react'
import { PageHeader, Loading, ErrorAlert } from '@/components/shared'
import { useLookups } from '@/hooks/useLookups'
import { useAuth } from '@/hooks/useAuth'

interface GroupDisplay {
  id: number
  code: string
  type: string // Will be determined from external data
  section: string
  module: string
  size: number
  instructor?: string
}

export const GroupeTPListPage: React.FC = () => {
  const navigate = useNavigate()
  const { user } = useAuth()
  const { groupesTp, sections, modules, isLoading, error, clearError, fetchModules } = useLookups()
  const [displayGroups, setDisplayGroups] = useState<GroupDisplay[]>([])
  const [filteredGroups, setFilteredGroups] = useState<GroupDisplay[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [groupTypeFilter, setGroupTypeFilter] = useState<string>('ALL')

  // Helper function to get badge styling based on session type
  const getTypeBadgeStyle = (type: string) => {
    const styles: Record<string, { bg: string; text: string; label: string }> = {
      CM: { bg: 'bg-purple-100', text: 'text-purple-800', label: 'Lecture (CM)' },
      TD: { bg: 'bg-green-100', text: 'text-green-800', label: 'Tutorial (TD)' },
      TP: { bg: 'bg-blue-100', text: 'text-blue-800', label: 'Practical (TP)' },
      EXAM: { bg: 'bg-red-100', text: 'text-red-800', label: 'Exam (EXAM)' },
      SEMINAR: { bg: 'bg-orange-100', text: 'text-orange-800', label: 'Seminar' },
    }
    return styles[type] || { bg: 'bg-gray-100', text: 'text-gray-800', label: type }
  }

  useEffect(() => {
    fetchModules()
    // Note: Groups loading requires section IDs - implement batch load if available
  }, [])

  useEffect(() => {
    // Convert GroupeTP to display format
    const groups: GroupDisplay[] = groupesTp.map((g) => {
      const section = sections.find((s) => s.id === g.section_id)
      const module = modules.find((m) => m.id === section?.module_id)
      // Use type from API, default to 'TP' if not provided
      const sessionType = g.type?.toUpperCase() || 'TP'
      return {
        id: g.id,
        code: g.code,
        type: sessionType,  // CM, TD, TP, EXAM, SEMINAR from API
        section: section?.name || `Section ${g.section_id}`,
        module: module?.name || 'Unknown Module',
        size: g.effectif,
      }
    })
    setDisplayGroups(groups)
  }, [groupesTp, sections, modules])

  useEffect(() => {
    let filtered = displayGroups
    if (groupTypeFilter !== 'ALL') {
      filtered = filtered.filter((g) => g.type === groupTypeFilter)
    }
    if (searchTerm) {
      filtered = filtered.filter(
        (g) =>
          g.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
          g.section.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }
    setFilteredGroups(filtered)
  }, [displayGroups, searchTerm, groupTypeFilter])

  const isServiceManager = user?.user_type === 'responsable_service'

  if (isLoading && groupesTp.length === 0) {
    return <Loading message="Loading TP groups..." />
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <PageHeader
          title="Groups (Groupes TP/TD/COURSE)"
          description="Manage practical work groups, tutorials, and course sections"
        />
        {isServiceManager && (
          <button
            onClick={() => navigate('/groupes/new')}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            <span>Add Group</span>
          </button>
        )}
      </div>

      {error && <ErrorAlert message={error} onDismiss={clearError} />}

      {/* Search and Filter Bar */}
      <div className="bg-white rounded-lg shadow p-4 space-y-4">
        <input
          type="text"
          placeholder="Search groups by code or section..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Group Type Filter */}
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setGroupTypeFilter('ALL')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              groupTypeFilter === 'ALL'
                ? 'bg-gray-200 text-gray-900'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-150'
            }`}
          >
            All Types
          </button>
          <button
            onClick={() => setGroupTypeFilter('CM')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              groupTypeFilter === 'CM'
                ? 'bg-purple-200 text-purple-900'
                : 'bg-purple-50 text-purple-700 hover:bg-purple-100'
            }`}
          >
            Courses (CM)
          </button>
          <button
            onClick={() => setGroupTypeFilter('TP')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              groupTypeFilter === 'TP'
                ? 'bg-blue-200 text-blue-900'
                : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
            }`}
          >
            Practical (TP)
          </button>
          <button
            onClick={() => setGroupTypeFilter('TD')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              groupTypeFilter === 'TD'
                ? 'bg-green-200 text-green-900'
                : 'bg-green-50 text-green-700 hover:bg-green-100'
            }`}
          >
            Tutorials (TD)
          </button>
          <button
            onClick={() => setGroupTypeFilter('EXAM')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              groupTypeFilter === 'EXAM'
                ? 'bg-red-200 text-red-900'
                : 'bg-red-50 text-red-700 hover:bg-red-100'
            }`}
          >
            Exams (EXAM)
          </button>
          <button
            onClick={() => setGroupTypeFilter('SEMINAR')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              groupTypeFilter === 'SEMINAR'
                ? 'bg-orange-200 text-orange-900'
                : 'bg-orange-50 text-orange-700 hover:bg-orange-100'
            }`}
          >
            Seminars (SEMINAR)
          </button>
        </div>
      </div>

      {/* Groups Table */}
      {filteredGroups.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <p className="text-gray-500">
            {searchTerm || groupTypeFilter !== 'ALL' ? 'No groups match your filters' : 'No groups available'}
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Code</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Type</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Section</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Module</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Size</th>
                  <th className="px-6 py-3 text-right text-sm font-semibold text-gray-900">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredGroups.map((groupe) => (
                  <tr key={groupe.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">{groupe.code}</td>
                    <td className="px-6 py-4 text-sm">
                      {(() => {
                        const badgeStyle = getTypeBadgeStyle(groupe.type)
                        return (
                          <span className={`px-3 py-1 rounded-full text-xs font-medium ${badgeStyle.bg} ${badgeStyle.text}`}>
                            {badgeStyle.label}
                          </span>
                        )
                      })()}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{groupe.section}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{groupe.module}</td>
                    <td className="px-6 py-4 text-sm">
                      <div className="flex items-center gap-1">
                        <Users className="w-4 h-4 text-gray-400" />
                        <span className="text-gray-600">{groupe.size}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => navigate(`/groupes/${groupe.id}`)}
                          className="inline-flex items-center gap-1 px-3 py-1 text-sm bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition-colors"
                        >
                          <Eye className="w-4 h-4" />
                          View
                        </button>
                        {isServiceManager && (
                          <>
                            <button
                              onClick={() => navigate(`/groupes/${groupe.id}/edit`)}
                              className="inline-flex items-center gap-1 px-3 py-1 text-sm bg-green-50 text-green-600 rounded hover:bg-green-100 transition-colors"
                            >
                              <Edit2 className="w-4 h-4" />
                              Edit
                            </button>
                            <button
                              onClick={() => {
                                if (confirm('Delete this group?')) {
                                  // Handle delete
                                }
                              }}
                              className="inline-flex items-center gap-1 px-3 py-1 text-sm bg-red-50 text-red-600 rounded hover:bg-red-100 transition-colors"
                            >
                              <Trash2 className="w-4 h-4" />
                              Delete
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
