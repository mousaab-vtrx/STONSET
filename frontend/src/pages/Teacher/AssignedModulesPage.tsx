import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Users, BookOpen, Calendar, Lock, ChevronRight, Info } from 'lucide-react'
import { PageHeader, Loading, ErrorAlert } from '@/components/shared'
import { useLookups } from '@/hooks/useLookups'
import { useAuth } from '@/hooks/useAuth'

interface TeacherModule {
  id: string
  code: string
  name: string
  isDefault: boolean
  sections: number
  groupCount: number
  studentCount: number
  nextCreneau?: {
    date: string
    time: string
    salle: string
  }
}

export const TeacherAssignedModulesPage: React.FC = () => {
  const navigate = useNavigate()
  const { user } = useAuth()
  const { modules, isLoading, error, clearError, fetchModules } = useLookups()
  const [teacherModules, setTeacherModules] = useState<TeacherModule[]>([])
  const [defaultModule, setDefaultModule] = useState<TeacherModule | null>(null)

  useEffect(() => {
    fetchModules()
  }, [])

  useEffect(() => {
    // In a real app, fetch from API endpoint specific to teacher
    // For now, using mock data - modules assigned to current user
    if (modules.length > 0) {
      const assigned = modules
        .filter((m) => m.enseignant_id === user?.id)
        .map((m) => ({
          id: m.id.toString(),
          code: m.code,
          name: m.name,
          isDefault: false, // Would come from backend
          sections: 2,
          groupCount: 4,
          studentCount: 120,
        }))

      setTeacherModules(assigned)
      const def = assigned.length > 0 ? assigned[0] : null
      setDefaultModule(def)
    }
  }, [modules, user])

  if (isLoading && teacherModules.length === 0) {
    return <Loading message="Loading your assigned modules..." />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="My Assigned Modules"
        description="View your teaching modules and quick access to manage groups and reservations"
      />

      {error && <ErrorAlert message={error} onDismiss={clearError} />}

      {/* Default Module Card (Read-only) */}
      {defaultModule && (
        <div className="bg-gradient-to-r from-purple-600 to-purple-700 rounded-lg shadow-lg p-6 text-white">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3">
              <Lock className="w-6 h-6" />
              <div>
                <p className="text-purple-100 text-sm font-medium">Default Module</p>
                <h2 className="text-2xl font-bold">{defaultModule.name}</h2>
                <p className="text-purple-200">{defaultModule.code}</p>
              </div>
            </div>
            <span className="px-3 py-1 bg-white bg-opacity-20 rounded-full text-sm font-medium">
              Read-only
            </span>
          </div>

          <div className="grid grid-cols-3 gap-4 pt-4 border-t border-purple-400 border-opacity-30">
            <div>
              <p className="text-purple-200 text-sm">Sections</p>
              <p className="text-2xl font-bold">{defaultModule.sections}</p>
            </div>
            <div>
              <p className="text-purple-200 text-sm">Groups</p>
              <p className="text-2xl font-bold">{defaultModule.groupCount}</p>
            </div>
            <div>
              <p className="text-purple-200 text-sm">Students</p>
              <p className="text-2xl font-bold">{defaultModule.studentCount}</p>
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-purple-400 border-opacity-30 flex items-start gap-2">
            <Info size={16} className="flex-shrink-0 mt-0.5" />
            <p className="text-sm text-purple-200">
              Your default module cannot be changed. Contact your department head if changes are needed.
            </p>
          </div>

          <button
            onClick={() => navigate(`/modules/${defaultModule.id}/groups`)}
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-white text-purple-700 font-medium rounded hover:bg-purple-50 transition-colors"
          >
            <span>Manage Groups</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Other Assigned Modules */}
      {teacherModules.filter((m) => !m.isDefault).length > 0 && (
        <>
          <h3 className="text-xl font-bold text-gray-900 mt-8">Other Assigned Modules</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {teacherModules
              .filter((m) => !m.isDefault)
              .map((module) => (
                <div
                  key={module.id}
                  className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer"
                  onClick={() => navigate(`/modules/${module.id}`)}
                >
                  <div className="flex items-start gap-3 mb-4">
                    <BookOpen className="w-5 h-5 text-blue-600 flex-shrink-0 mt-1" />
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-gray-900">{module.name}</h3>
                      <p className="text-sm text-gray-500">{module.code}</p>
                    </div>
                  </div>

                  <div className="space-y-3 mb-4">
                    <div className="flex items-center gap-2 text-gray-600">
                      <Users className="w-4 h-4" />
                      <span className="text-sm">{module.groupCount} groups</span>
                    </div>
                    <div className="flex items-center gap-2 text-gray-600">
                      <Calendar className="w-4 h-4" />
                      <span className="text-sm">{module.studentCount} students</span>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        navigate(`/modules/${module.id}/groups`)
                      }}
                      className="flex-1 px-3 py-2 text-sm bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition-colors font-medium"
                    >
                      Manage Groups
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        navigate('/reservations/new', { state: { moduleId: module.id } })
                      }}
                      className="flex-1 px-3 py-2 text-sm bg-green-50 text-green-600 rounded hover:bg-green-100 transition-colors font-medium"
                    >
                      New Reservation
                    </button>
                  </div>
                </div>
              ))}
          </div>
        </>
      )}

      {teacherModules.length === 0 && !defaultModule && (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <BookOpen className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-600 text-lg">No modules assigned yet</p>
          <p className="text-gray-500 text-sm mt-1">
            Contact your department head to be assigned to modules
          </p>
        </div>
      )}
    </div>
  )
}
