import React from 'react'
import { PageHeader } from '@/components/shared'
import { Mail, Phone } from 'lucide-react'

export const TermsOfServicePage: React.FC = () => {
  return (
    <div className="space-y-0 overflow-hidden">
      {/* Header Section */}
      <div className="bg-gradient-to-br from-indigo-600 via-indigo-700 to-indigo-800 text-white py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <PageHeader 
            title="Terms of Service" 
            description="Effective: March 2026 | Last updated: March 22, 2026"
          />
        </div>
      </div>

      <div className="px-4 sm:px-6 lg:px-8 py-16 bg-white dark:bg-gray-900">
        <div className="max-w-5xl mx-auto space-y-8">
          {/* Quick Links */}
          <div className="bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800 rounded-xl p-6 mb-8">
            <p className="text-sm text-indigo-600 dark:text-indigo-400 font-semibold mb-3">Quick Navigation</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
              {['Account Terms', 'Use Restrictions', 'Content Rights', 'Termination', 'Disclaimer', 'Limitations', 'Changes', 'Contact'].map((item) => (
                <a key={item} href={`#${item.toLowerCase().replace(/\s+/g, '-')}`} className="text-indigo-600 dark:text-indigo-400 hover:underline">
                  • {item}
                </a>
              ))}
            </div>
          </div>

          {/* 1. Account Terms */}
          <section id="account-terms" className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">1. Account Terms</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              When you create an account on STONSET, you must provide accurate, complete, and current information. You are responsible for maintaining the confidentiality of your password and account information. You agree to accept responsibility for all activities that occur under your account. You must notify us immediately of any unauthorized use of your account.
            </p>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              We reserve the right to refuse service to anyone for any reason at any time.
            </p>
          </section>

          {/* 2. Use License */}
          <section id="use-restrictions" className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">2. Use Restrictions</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
              You may not use STONSET for any unlawful or prohibited purpose. Specifically, you agree not to:
            </p>
            <ul className="space-y-3 text-gray-700 dark:text-gray-300">
              <li className="flex items-start gap-3">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold mt-1">•</span>
                <span>Violate any applicable laws or regulations in your jurisdiction</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold mt-1">•</span>
                <span>Infringe upon or violate our intellectual property rights or others' rights</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold mt-1">•</span>
                <span>Transmit malicious code, viruses, or harmful software</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold mt-1">•</span>
                <span>Attempt to gain unauthorized access to our systems or data</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold mt-1">•</span>
                <span>Harass, threaten, defame, or abuse other users</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold mt-1">•</span>
                <span>Reverse engineer, disassemble, or attempt to derive source code</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold mt-1">•</span>
                <span>Use automated scripts or tools to access or scrape our platform without permission</span>
              </li>
            </ul>
          </section>

          {/* 3. Content Rights */}
          <section id="content-rights" className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">3. Intellectual Property Rights</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              STONSET and all materials provided on the platform (including text, graphics, logos, images, audio, and video) are the property of STONSET or its content suppliers and are protected by international copyright and trademark laws. You may not reproduce, distribute, transmit, modify, or use any content without prior written permission.
            </p>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              Any content you submit to STONSET remains your property, but you grant us a worldwide, non-exclusive, royalty-free license to use, reproduce, and distribute your content in connection with our services.
            </p>
          </section>

          {/* 4. User Responsibilities */}
          <section id="termination" className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">4. User Responsibilities & Data Accuracy</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              You are solely responsible for ensuring the accuracy and completeness of all data you input into STONSET. This includes facility information, scheduling details, and user information. STONSET is not liable for errors, omissions, or consequences arising from inaccurate data entry.
            </p>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              You must maintain regular backups of critical data and not rely solely on STONSET as your primary data repository without appropriate backup procedures.
            </p>
          </section>

          {/* 5. Disclaimer */}
          <section id="disclaimer" className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">5. Disclaimer of Warranties</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              STONSET IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. STONSET DISCLAIMS ALL WARRANTIES, INCLUDING IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. We make no warranty that STONSET will be uninterrupted, error-free, secure, or that defects will be corrected.
            </p>
          </section>

          {/* 6. Limitation of Liability */}
          <section id="limitations" className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">6. Limitation of Liability</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
              TO THE MAXIMUM EXTENT PERMITTED BY LAW, STONSET SHALL NOT BE LIABLE FOR:
            </p>
            <ul className="space-y-2 text-gray-700 dark:text-gray-300">
              <li className="flex items-start gap-3">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold mt-1">•</span>
                <span>Any indirect, incidental, special, consequential, or punitive damages</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold mt-1">•</span>
                <span>Loss of profits, data, or revenue arising from use of STONSET</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold mt-1">•</span>
                <span>Business interruption or loss of business opportunity</span>
              </li>
            </ul>
          </section>

          {/* 7. Termination */}
          <section id="changes" className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">7. Termination & Account Suspension</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              We may terminate or suspend your account and access to STONSET immediately, without notice, for any reason, including if you violate these Terms. Upon termination, your right to use STONSET ceases immediately. We are not responsible for any loss of data resulting from termination.
            </p>
          </section>

          {/* 8. Changes to Terms */}
          <section id="changes-to-terms" className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">8. Changes to Terms</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              STONSET reserves the right to modify these Terms at any time. Changes will be effective immediately upon posting to the platform. Your continued use of STONSET after any changes constitutes your acceptance of the new Terms.
            </p>
          </section>

          {/* 9. Governing Law */}
          <section className="space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">9. Governing Law</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              These Terms are governed by and construed in accordance with the laws of Morocco, without regard to its conflict of law provisions. You agree to submit to the exclusive jurisdiction of the courts located in Morocco.
            </p>
          </section>

          {/* Contact Section */}
          <section className="bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800 rounded-xl p-8 space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Questions About These Terms?</h2>
            <p className="text-gray-700 dark:text-gray-300">
              If you have any questions or concerns about these Terms of Service, please don't hesitate to contact us:
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <a 
                href="mailto:mousaabelharmali31@gmail.com"
                className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-all duration-300 hover:shadow-lg"
              >
                <Mail size={20} />
                Email Us
              </a>
              <a 
                href="tel:+212657288139"
                className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-all duration-300 hover:shadow-lg"
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
