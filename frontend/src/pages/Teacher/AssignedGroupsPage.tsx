import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Users, BookOpen, Users2, AlertCircle, Pencil, Calendar, Building2, Beaker } from 'lucide-react'
import { PageHeader, Loading, ErrorAlert } from '@/components/shared'
import { useLookups } from '@/hooks/useLookups'

interface GroupAssignment {
  id: number
  code: string
  type: 'CM' | 'TP' | 'TD' | 'EXAM' | 'SEMINAR'
  section: string
  module: string
  size: number
  schedule?: string
  salle?: string
}

export const TeacherAssignedGroupsPage: React.FC = () => {
  const navigate = useNavigate()
  const { groupesTp, sections, modules, isLoading, error, clearError, fetchModules } = useLookups()
  const [assignedGroups, setAssignedGroups] = useState<{
    course: GroupAssignment[]
    tp: GroupAssignment[]
    td: GroupAssignment[]
  }>({ course: [], tp: [], td: [] })

  useEffect(() => {
    fetchModules()
  }, [])

  useEffect(() => {
    // Convert GroupeTP to display format grouped by type
    const groups: GroupAssignment[] = groupesTp.map((g) => {
      const section = sections.find((s) => s.id === g.section_id)
      const module = modules.find((m) => m.id === section?.module_id)
      // Use type from API, normalize to uppercase
      const sessionType = (g.type?.toUpperCase() || 'TP') as 'CM' | 'TP' | 'TD' | 'EXAM' | 'SEMINAR'
      return {
        id: g.id,
        code: g.code,
        type: sessionType,
        section: section?.name || `Section ${g.section_id}`,
        module: module?.name || 'Unknown Module',
        size: g.effectif,
      }
    })

    const organized = {
      course: groups.filter((g) => g.type === 'CM'),
      tp: groups.filter((g) => g.type === 'TP' || g.type === 'TD' || g.type === 'EXAM' || g.type === 'SEMINAR'),
      td: groups.filter((g) => g.type === 'TD'),
    }
    setAssignedGroups(organized)
  }, [groupesTp, sections, modules])

  if (isLoading && !groupesTp.length) {
    return <Loading message="Loading your assigned groups..." />
  }

  const renderGroupSection = (title: string, icon: React.ReactNode, groups: GroupAssignment[], color: string) => {
    const getColorClasses = (colorBase: string) => {
      const colors: Record<string, { bg: string; text: string; light: string }> = {
        blue: { bg: 'bg-blue-600', text: 'text-blue-600', light: 'bg-blue-50' },
        purple: { bg: 'bg-purple-600', text: 'text-purple-600', light: 'bg-purple-50' },
        green: { bg: 'bg-green-600', text: 'text-green-600', light: 'bg-green-50' },
      }
      return colors[colorBase]
    }

    const colors = getColorClasses(color)

    return (
      <div className="space-y-4">
        <h3 className={`flex items-center gap-2 text-lg font-bold ${colors.text}`}>
          {icon}
          <span>{title}</span>
          <span className="ml-auto px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-700">
            {groups.length}
          </span>
        </h3>

        {groups.length === 0 ? (
          <div className={`${colors.light} rounded-lg p-6 text-center`}>
            <Users2 className="w-8 h-8 text-gray-400 mx-auto mb-2" />
            <p className={`${colors.text} font-medium`}>No {title.toLowerCase()} assigned</p>
            <p className="text-sm text-gray-500 mt-1">
              You can manage group assignments from the Groups management page
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {groups.map((group) => (
              <div
                key={group.id}
                className={`${colors.light} rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer`}
                onClick={() => navigate(`/groupes/${group.id}`)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-900">{group.code}</h4>
                    <div className="mt-2 space-y-1 text-sm text-gray-600">
                      <div className="flex items-center gap-2">
                        <BookOpen className="w-4 h-4" />
                        <span>{group.module}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Users className="w-4 h-4" />
                        <span>{group.size} students</span>
                      </div>
                      {group.schedule && (
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4" />
                          <span>{group.schedule}</span>
                        </div>
                      )}
                      {group.salle && (
                        <div className="flex items-center gap-2">
                          <Building2 className="w-4 h-4" />
                          <span>{group.salle}</span>
                        </div>
                      )}"
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      navigate(`/groupes/${group.id}/students`)
                    }}
                    className={`${colors.light} ${colors.text} px-3 py-2 text-sm font-medium rounded hover:bg-opacity-70 transition-all`}
                  >
                    View Roster
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    )
  }

  const totalGroups =
    assignedGroups.course.length + assignedGroups.tp.length + assignedGroups.td.length

  return (
    <div className="space-y-6">
      <PageHeader
        title="My Assigned Groups"
        description="Manage course sections, practical work groups, and tutorial classes"
      />

      {error && <ErrorAlert message={error} onDismiss={clearError} />}

      {/* Summary Stats */}
      {totalGroups > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg shadow p-4">
            <p className="text-gray-600 text-sm">Total Groups</p>
            <p className="text-3xl font-bold text-gray-900 mt-1">{totalGroups}</p>
          </div>
          <div className="bg-purple-50 rounded-lg shadow p-4">
            <p className="text-purple-600 text-sm">Course Sections</p>
            <p className="text-3xl font-bold text-purple-600 mt-1">{assignedGroups.course.length}</p>
          </div>
          <div className="bg-blue-50 rounded-lg shadow p-4">
            <p className="text-blue-600 text-sm">Practical Work</p>
            <p className="text-3xl font-bold text-blue-600 mt-1">{assignedGroups.tp.length}</p>
          </div>
          <div className="bg-green-50 rounded-lg shadow p-4">
            <p className="text-green-600 text-sm">Tutorials</p>
            <p className="text-3xl font-bold text-green-600 mt-1">{assignedGroups.td.length}</p>
          </div>
        </div>
      )}

      {/* Groups by Type */}
      <div className="space-y-8">
        {renderGroupSection(
          'Course Sections',
          <BookOpen className="w-6 h-6" />,
          assignedGroups.course,
          'purple'
        )}

        {renderGroupSection(
          'Practical Work Groups (TP)',
          <Beaker className="w-6 h-6" />,
          assignedGroups.tp,
          'blue'
        )}

        {renderGroupSection(
          'Tutorial Classes (TD)',
          <Pencil size={24} />,
          assignedGroups.td,
          'green'
        )}
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex gap-3">
        <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div className="text-sm text-blue-700">
          <p className="font-medium mb-1">Managing Groups</p>
          <p>
            To request assignment to new groups or modify your group assignments, contact your department
            head or visit the Groups management page.
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      {totalGroups > 0 && (
        <div className="bg-white rounded-lg shadow p-6 space-y-3">
          <h3 className="font-bold text-gray-900">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <button
              onClick={() => navigate('/reservations/new')}
              className="px-4 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors"
            >
              Create Reservation
            </button>
            <button
              onClick={() => navigate('/reservations')}
              className="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              View My Reservations
            </button>
            <button
              onClick={() => navigate('/groupes')}
              className="px-4 py-2 bg-gray-600 text-white font-medium rounded-lg hover:bg-gray-700 transition-colors"
            >
              Browse All Groups
            </button>
          </div>
        </div>
      )}

      {totalGroups === 0 && (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <Users2 className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-600 text-lg">No groups assigned yet</p>
          <p className="text-gray-500 text-sm mt-1">Contact your department head to be assigned to groups</p>
          <button
            onClick={() => navigate('/groupes')}
            className="mt-4 inline-block px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            Browse All Groups
          </button>
        </div>
      )}
    </div>
  )
}
