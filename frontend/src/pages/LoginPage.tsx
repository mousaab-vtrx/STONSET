import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { useToast } from '@/hooks/useToast'
import { ErrorAlert, Loading } from '@/components/shared'

export const LoginPage: React.FC = () => {
  const navigate = useNavigate()
  const { login, isLoading, error, isLoggedIn } = useAuth()
  const { success } = useToast()

  // Redirect to dashboard if already logged in
  useEffect(() => {
    console.log('LoginPage useEffect - isLoggedIn:', isLoggedIn)
    if (isLoggedIn) {
      console.log('Already logged in, redirecting to dashboard')
      navigate('/dashboard', { replace: true })
    }
  }, [isLoggedIn, navigate])

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const result = await login(formData.email, formData.password)
    if (result) {
      success('Login successful!')
      // Don't navigate here - let the useEffect handle it when state updates
      // The router will automatically redirect when isLoggedIn becomes true
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center px-4 overflow-hidden">
      {/* Background Image with Overlay */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url('/images/pexels-pavel-danilyuk-8423051.jpg')`,
        }}
      >
        {/* Dark Overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900/70 via-blue-900/60 to-purple-900/70"></div>
        
        {/* Animated Blur Overlay */}
        <div className="absolute inset-0 backdrop-blur-sm opacity-30"></div>
      </div>

      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-10 left-10 w-40 h-40 bg-blue-400 rounded-full mix-blend-screen filter blur-3xl opacity-15 animate-blob"></div>
        <div className="absolute top-40 right-10 w-40 h-40 bg-purple-400 rounded-full mix-blend-screen filter blur-3xl opacity-15 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-40 h-40 bg-indigo-400 rounded-full mix-blend-screen filter blur-3xl opacity-15 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 w-full max-w-md animate-fade-in">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-24 h-24 mx-auto mb-4 flex items-center justify-center transform hover:scale-110 transition-transform duration-300">
            <img src="/images/logonobackground.png" alt="STONSET" className="w-24 h-24 object-contain" />
          </div>
          <h1 className="text-4xl font-bold mb-2 text-white drop-shadow-lg">Welcome Back</h1>
          <p className="text-blue-100 drop-shadow-md">Sign in to your account to continue</p>
        </div>

        {/* Login Card */}
        <div className="bg-white/95 dark:bg-gray-900/95 rounded-2xl shadow-2xl backdrop-blur-xl p-8 border border-white/20 dark:border-gray-700/50">
          {/* Error Message */}
          {error && <ErrorAlert message={error} title="Authentication Error" />}

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                placeholder="you@example.com"
                className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all dark:bg-gray-800 dark:text-white"
                value={formData.email}
                onChange={handleInputChange}
                required
                disabled={isLoading}
              />
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                Password
              </label>
              <input
                type="password"
                name="password"
                placeholder="Enter your password"
                className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all dark:bg-gray-800 dark:text-white"
                value={formData.password}
                onChange={handleInputChange}
                required
                disabled={isLoading}
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full py-3 px-4 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center transform hover:scale-105"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loading size="sm" />
                  <span className="ml-2">Signing in...</span>
                </>
              ) : (
                'Sign In'
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

          {/* Register Link */}
          <p className="text-center text-sm text-gray-700 dark:text-gray-300">
            Don't have an account?
            <Link to="/register" className="ml-2 font-semibold text-indigo-600 hover:text-indigo-700 dark:text-indigo-400 dark:hover:text-indigo-300 transition-colors">
              Create one now
            </Link>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-blue-100 drop-shadow-md mt-8">
          Having trouble signing in?
          <a href="#" className="ml-2 font-semibold text-white hover:text-blue-200 transition-colors">
            Contact support
          </a>
        </p>
      </div>
    </div>
  )
}
