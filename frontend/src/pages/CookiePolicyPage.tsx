import React from 'react'
import { PageHeader } from '@/components/shared'
import { Mail, Phone, Cookie } from 'lucide-react'

export const CookiePolicyPage: React.FC = () => {
  return (
    <div className="space-y-0 overflow-hidden">
      {/* Header Section */}
      <div className="bg-gradient-to-br from-orange-600 via-orange-700 to-orange-800 text-white py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <PageHeader 
            title="Cookie Policy" 
            description="Effective: March 2026 | Last updated: March 22, 2026"
          />
        </div>
      </div>

      <div className="px-4 sm:px-6 lg:px-8 py-16 bg-white dark:bg-gray-900">
        <div className="max-w-5xl mx-auto space-y-8">
          {/* Info Callout */}
          <div className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-xl p-6">
            <p className="text-orange-900 dark:text-orange-200">
              <strong>Transparency First:</strong> We use cookies to make STONSET work better for you. This policy explains what cookies are, why we use them, and how you can control them.
            </p>
          </div>

          {/* 1. What Are Cookies */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-3 mb-4">
              <Cookie className="text-orange-600 dark:text-orange-400" size={28} />
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">1. What Are Cookies?</h2>
            </div>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              Cookies are small text files stored on your device (computer, tablet, or mobile phone) when you visit a website. They serve several important purposes: remembering your login information, storing your preferences, tracking how you use our platform to improve it, and helping us understand user behavior patterns.
            </p>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mt-4">
              Most websites use cookies. They're a standard part of how the internet works. We use cookies to make STONSET more functional, secure, and user-friendly.
            </p>
          </section>

          {/* 2. Types of Cookies We Use */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">2. Types of Cookies We Use</h2>
            
            <div className="space-y-6">
              <div className="bg-gray-50 dark:bg-gray-800 p-5 rounded-lg">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">🔐 Essential/Functional Cookies</h3>
                <p className="text-gray-700 dark:text-gray-300 mb-2">
                  <strong>Purpose:</strong> Necessary for STONSET to function properly
                </p>
                <p className="text-gray-700 dark:text-gray-300 mb-2">
                  <strong>Examples:</strong> Session tokens, authentication cookies, CSRF protection, language preferences
                </p>
                <p className="text-gray-700 dark:text-gray-300">
                  <strong>Can be disabled?</strong> No - disabling these will prevent login and core functionality
                </p>
              </div>

              <div className="bg-gray-50 dark:bg-gray-800 p-5 rounded-lg">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">📊 Analytics Cookies</h3>
                <p className="text-gray-700 dark:text-gray-300 mb-2">
                  <strong>Purpose:</strong> Help us understand how users interact with STONSET
                </p>
                <p className="text-gray-700 dark:text-gray-300 mb-2">
                  <strong>Examples:</strong> Page views, click tracking, feature usage patterns, error logging
                </p>
                <p className="text-gray-700 dark:text-gray-300">
                  <strong>Can be disabled?</strong> Yes - you can opt-out of analytics without affecting core services
                </p>
              </div>

              <div className="bg-gray-50 dark:bg-gray-800 p-5 rounded-lg">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">⚙️ Preference Cookies</h3>
                <p className="text-gray-700 dark:text-gray-300 mb-2">
                  <strong>Purpose:</strong> Remember your choices and settings
                </p>
                <p className="text-gray-700 dark:text-gray-300 mb-2">
                  <strong>Examples:</strong> Dark mode preference, notification settings, UI layout choices
                </p>
                <p className="text-gray-700 dark:text-gray-300">
                  <strong>Can be disabled?</strong> Yes - but your preferences will reset on each visit
                </p>
              </div>
            </div>
          </section>

          {/* 3. Cookie Duration */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">3. Cookie Duration</h2>
            <div className="space-y-3 text-gray-700 dark:text-gray-300">
              <div className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400 font-bold mt-1">•</span>
                <span><strong>Session Cookies:</strong> Expire when you close your browser; used for active login sessions</span>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400 font-bold mt-1">•</span>
                <span><strong>Persistent Cookies:</strong> Remain on your device for a set period (typically 1-2 years); used for "remember me" features and preferences</span>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400 font-bold mt-1">•</span>
                <span><strong>Third-party Cookies:</strong> None intentionally set by STONSET, but your browser may contain cookies from other domains you've visited</span>
              </div>
            </div>
          </section>

          {/* 4. How to Control Cookies */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">4. How to Control & Delete Cookies</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
              You have full control over cookies on your device. Most modern browsers allow you to:
            </p>
            <ul className="space-y-2 text-gray-700 dark:text-gray-300 mb-4">
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400 font-bold mt-1">•</span>
                <span>View which cookies are stored on your device</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400 font-bold mt-1">•</span>
                <span>Delete cookies individually or all at once</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400 font-bold mt-1">•</span>
                <span>Set preferences for which websites can place cookies</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400 font-bold mt-1">•</span>
                <span>Enable "Do Not Track" signals</span>
              </li>
            </ul>
            <div className="bg-gray-50 dark:bg-gray-800 p-5 rounded-lg">
              <p className="text-gray-700 dark:text-gray-300 font-semibold mb-2">Browser Settings:</p>
              <ul className="space-y-1 text-sm text-gray-700 dark:text-gray-300">
                <li>• <strong>Chrome:</strong> Settings → Privacy and security → Cookies and other site data</li>
                <li>• <strong>Firefox:</strong> Preferences → Privacy & Security → Cookies and Site Data</li>
                <li>• <strong>Safari:</strong> Preferences → Privacy → Cookies and website data</li>
                <li>• <strong>Edge:</strong> Settings → Privacy, search, and services → Clear browsing data</li>
              </ul>
            </div>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mt-4">
              <strong>⚠️ Important:</strong> Disabling ALL cookies may prevent STONSET from working correctly, including login functionality. We recommend only blocking non-essential cookies while keeping essential ones enabled.
            </p>
          </section>

          {/* 5. Local Storage & Similar Technology */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">5. Other Tracking Technologies</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
              Beyond cookies, we may use similar technologies:
            </p>
            <ul className="space-y-2 text-gray-700 dark:text-gray-300">
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400 font-bold mt-1">•</span>
                <span><strong>Local Storage:</strong> Browser-based storage similar to cookies but with larger capacity</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400 font-bold mt-1">•</span>
                <span><strong>Session Storage:</strong> Temporary storage cleared when you close the browser</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400 font-bold mt-1">•</span>
                <span><strong>Pixels & Beacons:</strong> Small transparent images used to track page views</span>
              </li>
            </ul>
          </section>

          {/* 6. Your Choices & Rights */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">6. Your Choices & Rights</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              We respect your privacy choices. You can:
            </p>
            <ul className="space-y-3 text-gray-700 dark:text-gray-300 mt-4">
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400">✓</span>
                <span>Disable non-essential cookies without affecting core STONSET functionality</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400">✓</span>
                <span>Request a copy of the cookies and tracking data we have about you</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400">✓</span>
                <span>Request deletion of tracking data</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-orange-600 dark:text-orange-400">✓</span>
                <span>Update your cookie preferences at any time</span>
              </li>
            </ul>
          </section>

          {/* 7. Changes to This Policy */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">7. Changes to This Cookie Policy</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              We may update this policy to reflect changes in our practices or technology. When we make material changes, we'll update the "Last Updated" date and notify you through STONSET or email.
            </p>
          </section>

          {/* Contact Section */}
          <section className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-xl p-8 space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Questions About Our Cookies?</h2>
            <p className="text-gray-700 dark:text-gray-300">
              If you have questions about how STONSET uses cookies or want to manage your cookie preferences:
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <a 
                href="mailto:mousaabelharmali31@gmail.com"
                className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white font-semibold rounded-lg transition-all duration-300 hover:shadow-lg"
              >
                <Mail size={20} />
                Email Us
              </a>
              <a 
                href="tel:+212657288139"
                className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white font-semibold rounded-lg transition-all duration-300 hover:shadow-lg"
              >
                <Phone size={20} />
                Call +212 657 288 139
              </a>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}
