import React from 'react'
import { PageHeader } from '@/components/shared'
import { Mail, Phone, Lock, Eye, Share2 } from 'lucide-react'

export const PrivacyPolicyPage: React.FC = () => {
  return (
    <div className="space-y-0 overflow-hidden">
      {/* Header Section */}
      <div className="bg-gradient-to-br from-emerald-600 via-emerald-700 to-emerald-800 text-white py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <PageHeader 
            title="Privacy Policy" 
            description="Effective: March 2026 | Last updated: March 22, 2026"
          />
        </div>
      </div>

      <div className="px-4 sm:px-6 lg:px-8 py-16 bg-white dark:bg-gray-900">
        <div className="max-w-5xl mx-auto space-y-8">
          {/* Info Callout */}
          <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl p-6">
            <p className="text-amber-900 dark:text-amber-200">
              <strong>Your Privacy Matters:</strong> STONSET is committed to protecting your personal information and ensuring transparency about how we use your data. This Privacy Policy explains our practices.
            </p>
          </div>

          {/* 1. Types of Information We Collect */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-3 mb-4">
              <Eye className="text-emerald-600 dark:text-emerald-400" size={28} />
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">1. Types of Information We Collect</h2>
            </div>
            
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Personal Data Provided Directly</h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li className="flex items-start gap-3">
                    <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                    <span><strong>Account Information:</strong> Name, email address, password, phone number, institution affiliation</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                    <span><strong>Facility Data:</strong> Building information, room details, capacity, equipment, scheduling information</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                    <span><strong>Reservation Details:</strong> Booking times, duration, attendee information, purposes for facility use</span>
                  </li>
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Automatically Collected Data</h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li className="flex items-start gap-3">
                    <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                    <span><strong>Usage Data:</strong> Pages visited, time spent, click patterns, search queries, error reports</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                    <span><strong>Device Information:</strong> IP address, browser type, operating system, device identifiers</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                    <span><strong>Location Data:</strong> Derived from IP address (city/country level, not precise location)</span>
                  </li>
                </ul>
              </div>
            </div>
          </section>

          {/* 2. How We Use Your Data */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">2. How We Use Your Information</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">We use your information for:</p>
            <ul className="space-y-3 text-gray-700 dark:text-gray-300">
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400">✓</span>
                <span><strong>Service Delivery:</strong> Creating and managing your account, processing reservations, scheduling facilities</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400">✓</span>
                <span><strong>Communication:</strong> Sending updates, confirmations, and support-related messages</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400">✓</span>
                <span><strong>Service Improvement:</strong> Analyzing usage patterns to improve features and user experience</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400">✓</span>
                <span><strong>Security & Compliance:</strong> Detecting fraud, preventing abuse, ensuring legal compliance</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400">✓</span>
                <span><strong>Analytics & Reporting:</strong> Generating usage reports and facility utilization insights</span>
              </li>
            </ul>
          </section>

          {/* 3. Data Sharing & Disclosure */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">3. Data Sharing & Disclosure</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
              We do NOT sell your personal information. We may share data only when:
            </p>
            <ul className="space-y-2 text-gray-700 dark:text-gray-300">
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span>Required by law or legal process</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span>Necessary to provide our services (e.g., facility managers seeing reservation details)</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span>You explicitly consent to sharing</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span>With trusted service providers who process data on our behalf under strict confidentiality agreements</span>
              </li>
            </ul>
          </section>

          {/* 4. Data Security */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-3 mb-4">
              <Lock className="text-emerald-600 dark:text-emerald-400" size={28} />
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">4. Data Security</h2>
            </div>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
              We implement industry-standard security measures including:
            </p>
            <ul className="space-y-2 text-gray-700 dark:text-gray-300">
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span>Encryption of data in transit and at rest (SSL/TLS protocols)</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span>Secure authentication mechanisms and password hashing</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span>Regular security audits and penetration testing</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span>Access controls limiting employee data access</span>
              </li>
            </ul>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mt-4">
              <strong>Note:</strong> No system is 100% secure. While we strive to protect your information, we cannot guarantee absolute security.
            </p>
          </section>

          {/* 5. Your Rights */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">5. Your Privacy Rights</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
              Depending on your location, you may have the following rights:
            </p>
            <ul className="space-y-3 text-gray-700 dark:text-gray-300">
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span><strong>Access:</strong> Request a copy of your personal data</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span><strong>Correction:</strong> Correct inaccurate or incomplete information</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span><strong>Deletion:</strong> Request deletion of your data ("right to be forgotten")</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span><strong>Portability:</strong> Export your data in a machine-readable format</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">•</span>
                <span><strong>Opt-out:</strong> Withdraw consent to processing at any time</span>
              </li>
            </ul>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mt-4">
              To exercise these rights, contact us using the information provided at the end of this policy.
            </p>
          </section>

          {/* 6. Data Retention */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">6. Data Retention</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              We retain personal data only as long as necessary to provide our services and comply with legal obligations. Account data is typically retained while your account is active and for 30 days after deletion. Historical reservation data for audit purposes may be retained for up to 7 years as required by institutional policies.
            </p>
          </section>

          {/* 7. Changes to Policy */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">7. Changes to This Privacy Policy</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              We may update this Privacy Policy periodically. We'll notify you of material changes by updating the "Last Updated" date and, when required, obtaining your consent. Your continued use of STONSET after changes constitutes your acceptance of the updated policy.
            </p>
          </section>

          {/* Contact Section */}
          <section className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl p-8 space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Privacy Questions or Concerns?</h2>
            <p className="text-gray-700 dark:text-gray-300">
              If you have questions about this Privacy Policy or want to exercise your privacy rights:
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <a 
                href="mailto:mousaabelharmali31@gmail.com"
                className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-lg transition-all duration-300 hover:shadow-lg"
              >
                <Mail size={20} />
                Email Us
              </a>
              <a 
                href="tel:+212657288139"
                className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-lg transition-all duration-300 hover:shadow-lg"
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
