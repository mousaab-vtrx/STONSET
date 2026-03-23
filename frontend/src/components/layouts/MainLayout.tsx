import React, { useState, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Menu, LogOut, Settings } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { ThemeToggle } from '@/components/ThemeToggle'

interface MainLayoutProps {
  children: React.ReactNode
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const { user, isLoggedIn, logout } = useAuth()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col transition-colors duration-200">
      {/* Navigation Bar */}
      <nav className="bg-white dark:bg-gray-800 shadow sticky top-0 z-40 border-b border-gray-200 dark:border-gray-700" role="navigation" aria-label="Main navigation">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 sm:h-20">
            {/* Logo / Brand */}
            <Link to="/" className="flex items-center gap-3 hover:opacity-90 transition-opacity">
              <img 
                src="/images/logonobackground.png" 
                alt="STONSET Logo" 
                className="h-16 sm:h-20 w-auto flex-shrink-0"
              />
              <div className="hidden sm:flex flex-col gap-0.5">
                <span className="text-base sm:text-lg font-bold text-gray-900 dark:text-white">STONSET</span>
                <span className="text-xs text-gray-500 dark:text-gray-400">Room Reservations</span>
              </div>
            </Link>

            {/* Desktop Navigation Menu */}
            <div className="hidden md:flex items-center gap-6">
              {isLoggedIn && (
                <nav className="flex gap-6 text-sm font-medium">
                  <Link
                    to="/dashboard"
                    className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/reservations"
                    className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                  >
                    Reservations
                  </Link>
                  <div className="relative group">
                    <button className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex items-center gap-1">
                      Resources
                      <span className="text-xs">▼</span>
                    </button>
                    <div className="absolute left-0 mt-0 w-48 bg-white dark:bg-gray-700 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 border border-gray-200 dark:border-gray-600">
                      <Link
                        to="/modules"
                        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-gray-600 first:rounded-t-lg"
                      >
                        Modules
                      </Link>
                      <Link
                        to="/salles"
                        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-gray-600"
                      >
                        TP Rooms
                      </Link>
                      <Link
                        to="/groupes"
                        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-gray-600 last:rounded-b-lg"
                      >
                        Groups
                      </Link>
                    </div>
                  </div>
                  <div className="relative group">
                    <button className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex items-center gap-1">
                      My Teaching
                      <span className="text-xs">▼</span>
                    </button>
                    <div className="absolute left-0 mt-0 w-48 bg-white dark:bg-gray-700 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 border border-gray-200 dark:border-gray-600">
                      <Link
                        to="/my-modules"
                        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-gray-600 first:rounded-t-lg"
                      >
                        My Modules
                      </Link>
                      <Link
                        to="/my-groups"
                        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-gray-600 last:rounded-b-lg"
                      >
                        My Groups
                      </Link>
                    </div>
                  </div>
                </nav>
              )}
            </div>

            {/* Right Side: User Menu / Login/Register */}
            <div className="flex items-center gap-2 sm:gap-4">
              {isLoggedIn ? (
                <>
                  {/* Mobile Menu Button */}
                  <button
                    onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                    className="md:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    <Menu size={24} />
                  </button>

                  {/* Theme Toggle */}
                  <ThemeToggle />

                  {/* User Avatar / Profile Dropdown */}
                  <div className="relative" ref={menuRef}>
                    <button
                      onClick={() => setUserMenuOpen(!userMenuOpen)}
                      className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    >
                      {user?.avatar_url ? (
                        <img
                          src={user.avatar_url}
                          alt={user.prenom_user}
                          className="w-8 h-8 rounded-full object-cover"
                        />
                      ) : (
                        <div className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center text-sm font-bold">
                          {user?.prenom_user.charAt(0)}{user?.nom_user.charAt(0)}
                        </div>
                      )}
                      <span className="hidden sm:inline text-sm font-medium text-gray-900 dark:text-white">
                        {user?.prenom_user}
                      </span>
                    </button>

                    {/* Dropdown Menu */}
                    {userMenuOpen && (
                      <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-700 rounded-lg shadow-lg z-50 border border-gray-200 dark:border-gray-600">
                        <Link
                          to="/profile"
                          className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 first:rounded-t-lg"
                        >
                          <Settings size={16} />
                          My Profile
                        </Link>
                        <Link
                          to="/settings"
                          className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600"
                        >
                          <Settings size={16} />
                          Settings
                        </Link>
                        <button
                          onClick={handleLogout}
                          className="w-full flex items-center gap-2 text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 last:rounded-b-lg"
                        >
                          <LogOut size={16} />
                          Logout
                        </button>
                      </div>
                    )}
                  </div>
                </>
              ) : (
                <div className="flex gap-3">
                  <Link
                    to="/login"
                    className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                  >
                    Sign In
                  </Link>
                  <Link
                    to="/register"
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                  >
                    Sign Up
                  </Link>
                </div>
              )}
            </div>
          </div>

          {/* Mobile Navigation Menu */}
          {mobileMenuOpen && isLoggedIn && (
            <div className="md:hidden pb-4 border-t border-gray-200 dark:border-gray-700">
              <Link
                to="/dashboard"
                className="block px-4 py-2 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded"
              >
                Dashboard
              </Link>
              <Link
                to="/reservations"
                className="block px-4 py-2 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded"
              >
                Reservations
              </Link>
              
              <div className="px-4 py-2 mt-2">
                <p className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">Resources</p>
                <Link
                  to="/modules"
                  className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded"
                >
                  Modules
                </Link>
                <Link
                  to="/salles"
                  className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded"
                >
                  TP Rooms
                </Link>
                <Link
                  to="/groupes"
                  className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded"
                >
                  Groups
                </Link>
              </div>

              <div className="px-4 py-2">
                <p className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">My Teaching</p>
                <Link
                  to="/my-modules"
                  className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded"
                >
                  My Modules
                </Link>
                <Link
                  to="/my-groups"
                  className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded"
                >
                  My Groups
                </Link>
              </div>

              <Link
                to="/profile"
                className="block px-4 py-2 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded"
              >
                My Profile
              </Link>
              <button
                onClick={handleLogout}
                className="w-full text-left px-4 py-2 text-base font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 text-gray-900 dark:text-gray-100">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 border-t border-gray-800 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="text-white font-bold mb-4">STONSET</h3>
              <p className="text-sm">Room and Resource Reservation Management System</p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link to="/" className="hover:text-white transition-colors">
                    Home
                  </Link>
                </li>
                {isLoggedIn && (
                  <>
                    <li>
                      <Link to="/dashboard" className="hover:text-white transition-colors">
                        Dashboard
                      </Link>
                    </li>
                    <li>
                      <Link to="/reservations" className="hover:text-white transition-colors">
                        Reservations
                      </Link>
                    </li>
                    <li>
                      <Link to="/modules" className="hover:text-white transition-colors">
                        Modules
                      </Link>
                    </li>
                    <li>
                      <Link to="/salles" className="hover:text-white transition-colors">
                        TP Rooms
                      </Link>
                    </li>
                    <li>
                      <Link to="/groupes" className="hover:text-white transition-colors">
                        Groups
                      </Link>
                    </li>
                    <li>
                      <Link to="/my-modules" className="hover:text-white transition-colors">
                        My Modules
                      </Link>
                    </li>
                    <li>
                      <Link to="/my-groups" className="hover:text-white transition-colors">
                        My Groups
                      </Link>
                    </li>
                  </>
                )}
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link to="/privacy-policy" className="hover:text-white transition-colors">
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link to="/terms-of-service" className="hover:text-white transition-colors">
                    Terms of Service
                  </Link>
                </li>
                <li>
                  <Link to="/cookie-policy" className="hover:text-white transition-colors">
                    Cookie Policy
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="mailto:support@example.com" className="hover:text-white transition-colors">
                    Contact Support
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-sm">
            <p>&copy; 2026 STONSET. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
