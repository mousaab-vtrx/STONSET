import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload } from 'lucide-react'
import { PageHeader, Loading } from '@/components/shared'
import { useAuth } from '@/hooks/useAuth'
import { useToast } from '@/hooks/useToast'
import { getInitials } from '@/utils/helpers'

export const UserProfilePage: React.FC = () => {
  const navigate = useNavigate()
  const { user, isLoading, updateProfile, uploadAvatar } = useAuth()
  const { success, error: showError } = useToast()
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState({
    nom_user: user?.nom_user || '',
    prenom_user: user?.prenom_user || '',
    email: user?.email || '',
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleAvatarChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const result = await uploadAvatar(file)
      if (result) {
        success('Avatar updated successfully!')
      } else {
        showError('Failed to upload avatar')
      }
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const result = await updateProfile(formData)
    if (result) {
      success('Profile updated successfully!')
      setIsEditing(false)
    } else {
      showError('Failed to update profile')
    }
  }

  const formatUserType = (type: string | undefined): string => {
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

  if (!user) {
    return <Loading message="Loading profile..." />
  }

  return (
    <div className="space-y-6">
      <PageHeader title="My Profile" description="View and manage your account information" />

      {/* Main Profile Card */}
      <div className="bg-white rounded-lg shadow p-6 md:p-10">
        {/* Avatar and User Info Section */}
        <div className="flex flex-col sm:flex-row gap-6 sm:gap-8 mb-8 pb-8 border-b border-gray-200">
          {/* Avatar Section */}
          <div className="flex flex-col items-center sm:items-start">
            <div className="relative mb-4">
              {user.avatar_url ? (
                <img
                  src={user.avatar_url}
                  alt={user.prenom_user}
                  className="w-24 h-24 rounded-full object-cover shadow-lg"
                />
              ) : (
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 text-white flex items-center justify-center text-3xl font-bold shadow-lg">
                  {getInitials(user?.prenom_user, user?.nom_user)}
                </div>
              )}
              <label className="absolute bottom-0 right-0 bg-blue-600 text-white rounded-full p-2 cursor-pointer hover:bg-blue-700 transition-colors shadow-md">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleAvatarChange}
                  className="hidden"
                  disabled={isLoading}
                />
                <Upload className="w-4 h-4" />
              </label>
            </div>
            <p className="text-xs text-gray-500 text-center">Change Avatar</p>
          </div>

          {/* User Info Section */}
          <div className="flex-1">
            <div className="mb-6">
              <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">
                {user?.nom_user} {user?.prenom_user}
              </h2>
              <p className="text-gray-600 mt-1">{user.email}</p>
            </div>

            <div className="space-y-4">
              <div>
                <span className="text-xs font-semibold uppercase tracking-wide block mb-1 text-gray-600">
                  User Type
                </span>
                <p className="text-lg font-medium text-gray-900">{formatUserType(user?.user_type)}</p>
              </div>
              <div>
                <span className="text-xs font-semibold uppercase tracking-wide block mb-1 text-gray-600">
                  Status
                </span>
                <div className="flex items-center gap-2">
                  <span
                    className={`w-3 h-3 rounded-full ${
                      user?.is_active ? 'bg-green-500' : 'bg-gray-300'
                    }`}
                  ></span>
                  <p className="text-lg font-medium text-gray-900">
                    {user?.is_active ? 'Active' : 'Inactive'}
                  </p>
                </div>
              </div>
              {user.management_code && (
                <div>
                  <span className="text-xs font-semibold uppercase tracking-wide block mb-1 text-gray-600">
                    Management Code
                  </span>
                  <p className="text-lg font-medium text-gray-900 font-mono">{user.management_code}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Account Details */}
        <div className="mb-8">
          <h3 className="text-xl font-bold mb-4 text-gray-900">Account Details</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide block mb-2">
                Email Address
              </span>
              <p className="text-base text-gray-900">{user?.email}</p>
            </div>
            <div>
              <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide block mb-2">
                Full Name
              </span>
              <p className="text-base text-gray-900">
                {user?.nom_user} {user?.prenom_user}
              </p>
            </div>
            <div>
              <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide block mb-2">
                User Type
              </span>
              <p className="text-base text-gray-900">{formatUserType(user?.user_type)}</p>
            </div>
            <div>
              <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide block mb-2">
                Account Status
              </span>
              <span
                className={`inline-block px-3 py-1 rounded-full font-semibold text-sm ${
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

        {isEditing ? (
          <form onSubmit={handleSubmit} className="space-y-4 mb-8">
            <h3 className="text-lg font-bold text-gray-900">Edit Profile</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                <input
                  type="text"
                  name="prenom_user"
                  value={formData.prenom_user}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={isLoading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                <input
                  type="text"
                  name="nom_user"
                  value={formData.nom_user}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={isLoading}
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
            </div>
            <div className="flex gap-4 pt-4">
              <button
                type="submit"
                disabled={isLoading}
                className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {isLoading ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                type="button"
                onClick={() => setIsEditing(false)}
                className="px-6 py-2 border-2 border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div className="flex gap-3 sm:gap-4 justify-start flex-col-reverse sm:flex-row">
            <button
              onClick={() => navigate('/settings')}
              className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Account Settings
            </button>
            <button
              onClick={() => setIsEditing(true)}
              className="px-6 py-2 border-2 border-blue-600 text-blue-600 font-medium rounded-lg hover:bg-blue-50 transition-colors"
            >
              Edit Profile
            </button>
            <button
              onClick={() => navigate('/dashboard')}
              className="px-6 py-2 border-2 border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
            >
              Back to Dashboard
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
