import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'

// Layouts
import { MainLayout } from '@/components/layouts/MainLayout'

// Pages - Auth
import { LoginPage } from '@/pages/LoginPage'
import { RegisterPage } from '@/pages/RegisterPage'

// Pages - Main
import { HomePage } from '@/pages/HomePage'
import { DashboardPage } from '@/pages/DashboardPage'
import { ReservationListPage } from '@/pages/ReservationListPage'
import { ReservationCreatePage } from '@/pages/ReservationCreatePage'
import { ReservationDetailPage } from '@/pages/ReservationDetailPage'
import { UserProfilePage } from '@/pages/UserProfilePage'
import { SettingsPage } from '@/pages/SettingsPage'
import { ComponentShowcase } from '@/pages/ComponentShowcase'

// Pages - Resources (Management)
import { ModuleListPage } from '@/pages/Modules/ModuleListPage'
import { SalleTPListPage } from '@/pages/Resources/SalleTPListPage'
import { GroupeTPListPage } from '@/pages/Resources/GroupeTPListPage'

// Pages - Teacher Features
import { TeacherAssignedModulesPage } from '@/pages/Teacher/AssignedModulesPage'
import { TeacherAssignedGroupsPage } from '@/pages/Teacher/AssignedGroupsPage'

// Pages - Legal
import { PrivacyPolicyPage } from '@/pages/PrivacyPolicyPage'
import { TermsOfServicePage } from '@/pages/TermsOfServicePage'
import { CookiePolicyPage } from '@/pages/CookiePolicyPage'

export const RouterConfig: React.FC = () => {
  const { isLoggedIn, isLoading } = useAuth()

  // Show loading state while checking initial authentication
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <Routes>
      {/* Public Auth Routes - without layout */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Protected Routes with Layout */}
      <Route
        path="/dashboard"
        element={
          isLoggedIn ? (
            <MainLayout>
              <DashboardPage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/reservations"
        element={
          isLoggedIn ? (
            <MainLayout>
              <ReservationListPage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/reservations/new"
        element={
          isLoggedIn ? (
            <MainLayout>
              <ReservationCreatePage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/reservations/:id"
        element={
          isLoggedIn ? (
            <MainLayout>
              <ReservationDetailPage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/profile"
        element={
          isLoggedIn ? (
            <MainLayout>
              <UserProfilePage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/settings"
        element={
          isLoggedIn ? (
            <MainLayout>
              <SettingsPage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      {/* Public Routes with Layout */}
      <Route
        path="/"
        element={
          <MainLayout>
            <HomePage />
          </MainLayout>
        }
      />
      <Route
        path="/components"
        element={
          <MainLayout>
            <ComponentShowcase />
          </MainLayout>
        }
      />
      <Route
        path="/privacy-policy"
        element={
          <MainLayout>
            <PrivacyPolicyPage />
          </MainLayout>
        }
      />
      <Route
        path="/terms-of-service"
        element={
          <MainLayout>
            <TermsOfServicePage />
          </MainLayout>
        }
      />
      <Route
        path="/cookie-policy"
        element={
          <MainLayout>
            <CookiePolicyPage />
          </MainLayout>
        }
      />

      {/* Resource Management Routes */}
      <Route
        path="/modules"
        element={
          isLoggedIn ? (
            <MainLayout>
              <ModuleListPage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/salles"
        element={
          isLoggedIn ? (
            <MainLayout>
              <SalleTPListPage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/groupes"
        element={
          isLoggedIn ? (
            <MainLayout>
              <GroupeTPListPage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      {/* Teacher Feature Routes */}
      <Route
        path="/my-modules"
        element={
          isLoggedIn ? (
            <MainLayout>
              <TeacherAssignedModulesPage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/my-groups"
        element={
          isLoggedIn ? (
            <MainLayout>
              <TeacherAssignedGroupsPage />
            </MainLayout>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      {/* Catch-all - redirect to home */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
