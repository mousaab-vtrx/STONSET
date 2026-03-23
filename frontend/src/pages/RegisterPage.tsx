import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { useToast } from '@/hooks/useToast'
import { ErrorAlert, Loading } from '@/components/shared'

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate()
  const { register, isLoading, error, isLoggedIn } = useAuth()
  const { success } = useToast()

  // Redirect to dashboard if already logged in
  useEffect(() => {
    if (isLoggedIn) {
      navigate('/dashboard', { replace: true })
    }
  }, [isLoggedIn, navigate])

  const [formData, setFormData] = useState({
    prenom_user: '',
    nom_user: '',
    email: '',
    password: '',
    confirmPassword: '',
    user_type: 'enseignant',
    management_code: '',
  })

  const [validationError, setValidationError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setValidationError(null)

    if (formData.password !== formData.confirmPassword) {
      setValidationError('Passwords do not match')
      return
    }

    if (formData.password.length < 8) {
      setValidationError('Password must be at least 8 characters long')
      return
    }

    const result = await register(
      formData.email,
      formData.password,
      formData.prenom_user,
      formData.nom_user
    )

    if (result) {
      success('Registration successful! Welcome to STONSET!')
      // Don't navigate here - let the useEffect handle it when state updates
      // The router will automatically redirect when isLoggedIn becomes true
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center px-4 py-8 overflow-hidden">
      {/* Background Image with Overlay */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url('/images/pexels-pavel-danilyuk-8423380.jpg')`,
        }}
      >
        {/* Dynamic Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/75 via-blue-900/70 to-indigo-900/75"></div>
        
        {/* Subtle Texture Overlay */}
        <div className="absolute inset-0 backdrop-blur-sm opacity-40"></div>
      </div>

      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-10 left-10 w-40 h-40 bg-purple-400 rounded-full mix-blend-screen filter blur-3xl opacity-15 animate-blob"></div>
        <div className="absolute top-40 right-10 w-40 h-40 bg-blue-400 rounded-full mix-blend-screen filter blur-3xl opacity-15 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-40 h-40 bg-pink-400 rounded-full mix-blend-screen filter blur-3xl opacity-15 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 w-full max-w-md animate-fade-in">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-24 h-24 mx-auto mb-4 flex items-center justify-center transform hover:scale-110 transition-transform duration-300">
            <img src="/images/logonobackground.png" alt="STONSET" className="w-24 h-24 object-contain" />
          </div>
          <h1 className="text-4xl font-bold mb-2 text-white drop-shadow-lg">Create Account</h1>
          <p className="text-purple-100 drop-shadow-md">Join STONSET and start managing your reservations</p>
        </div>

        {/* Register Card */}
        <div className="bg-white/95 dark:bg-gray-900/95 rounded-2xl shadow-2xl backdrop-blur-xl p-8 border border-white/20 dark:border-gray-700/50">
          {/* Error Messages */}
          {error && <ErrorAlert message={error} title="Registration Error" />}
          {validationError && <ErrorAlert message={validationError} title="Validation Error" />}

          {/* Register Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Name Fields */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                  First Name
                </label>
                <input
                  type="text"
                  name="prenom_user"
                  placeholder="John"
                  className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all dark:bg-gray-800 dark:text-white"
                  value={formData.prenom_user}
                  onChange={handleInputChange}
                  required
                  disabled={isLoading}
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                  Last Name
                </label>
                <input
                  type="text"
                  name="nom_user"
                  placeholder="Doe"
                  className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all dark:bg-gray-800 dark:text-white"
                  value={formData.nom_user}
                  onChange={handleInputChange}
                  required
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* Email Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                placeholder="you@example.com"
                className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all dark:bg-gray-800 dark:text-white"
                value={formData.email}
                onChange={handleInputChange}
                required
                disabled={isLoading}
              />
            </div>

            {/* Role Selection */}
            <div>
              <label className="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                Your Role
              </label>
              <select
                name="user_type"
                value={formData.user_type}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all dark:bg-gray-800 dark:text-white"
                disabled={isLoading}
              >
                <option value="enseignant">Teacher (Enseignant)</option>
                <option value="chef_dept">Department Head (Chef de Département)</option>
                <option value="responsable_service">Service Manager (Responsable du Service)</option>
              </select>
            </div>

            {/* Management Code (Optional) */}
            <div>
              <label className="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                Management Code <span className="text-xs text-gray-600 dark:text-gray-400">(Optional)</span>
              </label>
              <input
                type="text"
                name="management_code"
                placeholder="Enter code to join a management group"
                className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all dark:bg-gray-800 dark:text-white"
                value={formData.management_code}
                onChange={handleInputChange}
                disabled={isLoading}
              />
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-2">
                If you're joining under a manager, ask them for their management code
              </p>
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                Password
              </label>
              <input
                type="password"
                name="password"
                placeholder="At least 8 characters"
                className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all dark:bg-gray-800 dark:text-white"
                value={formData.password}
                onChange={handleInputChange}
                required
                disabled={isLoading}
              />
            </div>

            {/* Confirm Password Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                Confirm Password
              </label>
              <input
                type="password"
                name="confirmPassword"
                placeholder="Confirm your password"
                className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all dark:bg-gray-800 dark:text-white"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                required
                disabled={isLoading}
              />
            </div>

            {/* Terms Agreement */}
            <div className="flex items-center">
              <input
                type="checkbox"
                id="terms"
                className="w-4 h-4 border-2 border-gray-300 dark:border-gray-600 rounded focus:ring-2 focus:ring-purple-500 dark:bg-gray-800"
                required
              />
              <label htmlFor="terms" className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                I agree to the{' '}
                <Link to="/terms-of-service" className="text-purple-600 dark:text-purple-400 hover:underline font-semibold">
                  Terms of Service
                </Link>
                {' '}and{' '}
                <Link to="/privacy-policy" className="text-purple-600 dark:text-purple-400 hover:underline font-semibold">
                  Privacy Policy
                </Link>
              </label>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full py-3 px-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center mt-6 transform hover:scale-105"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loading size="sm" />
                  <span className="ml-2">Creating account...</span>
                </>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-8">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300 dark:border-gray-600"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white dark:bg-gray-900 text-gray-600 dark:text-gray-400">or</span>
            </div>
          </div>

          {/* Login Link */}
          <p className="text-center text-sm text-gray-700 dark:text-gray-300">
            Already have an account?
            <Link to="/login" className="ml-2 font-semibold text-purple-600 hover:text-purple-700 dark:text-purple-400 dark:hover:text-purple-300 transition-colors">
              Sign in instead
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
