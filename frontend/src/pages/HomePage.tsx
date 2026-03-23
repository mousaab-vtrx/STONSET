import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/ui'

const HomePage: React.FC = () => {
  const { isLoggedIn } = useAuth()
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  return (
    <div className="space-y-0 overflow-hidden">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white overflow-hidden min-h-screen flex items-center">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-20 right-10 w-72 h-72 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
          <div className="absolute bottom-20 left-10 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
          <div className="absolute top-1/2 left-1/2 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000"></div>
        </div>

        <div className="w-full relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
            {/* Text Content */}
            <div className={`space-y-8 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`}>
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-white leading-tight animate-slide-down">
                Streamline Facility Reservations
              </h1>
              <p className="text-xl md:text-2xl text-slate-300 leading-relaxed font-light animate-fade-in-delay">
                STONSET is the comprehensive platform for managing classroom, laboratory, and facility bookings in educational institutions. Designed for efficiency and transparency, it eliminates scheduling conflicts and maximizes resource utilization.
              </p>
              
              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 pt-6 animate-fade-in-delay-2">
                {!isLoggedIn && (
                  <>
                    <Link to="/register" className="flex-1 sm:flex-initial">
                      <Button variant="primary" size="lg" className="w-full bg-indigo-600 hover:bg-indigo-700 transform transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-indigo-500/50">
                        Get Started
                        <ArrowRight size={20} className="ml-2" />
                      </Button>
                    </Link>
                    <Link to="/login" className="flex-1 sm:flex-initial">
                      <Button variant="outline" size="lg" className="w-full border-slate-400 text-slate-300 hover:bg-slate-700 transform transition-all duration-300 hover:scale-105">
                        Sign In
                      </Button>
                    </Link>
                  </>
                )}
                {isLoggedIn && (
                  <Link to="/dashboard" className="flex-1 sm:flex-initial">
                    <Button variant="primary" size="lg" className="w-full bg-indigo-600 hover:bg-indigo-700 transform transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-indigo-500/50">
                      Access Dashboard
                      <ArrowRight size={20} className="ml-2" />
                    </Button>
                  </Link>
                )}
              </div>
            </div>

            {/* Featured Image */}
            <div className={`hidden lg:block transition-all duration-1000 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-10'}`}>
              <div className="relative rounded-3xl overflow-hidden shadow-2xl group">
                <img 
                  src="/images/pexels-black-ice-551383-1314544.jpg" 
                  alt="Professional scheduling interface" 
                  className="w-full h-auto object-cover transform transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-tr from-indigo-600/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-3xl"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="relative py-24 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-900 overflow-hidden">
        <div className="w-full relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center max-w-7xl mx-auto">
            {/* Image */}
            <div className="hidden lg:block order-2 lg:order-1">
              <div className="group relative overflow-hidden rounded-3xl shadow-2xl">
                <img 
                  src="/images/pexels-pavel-danilyuk-8423051.jpg" 
                  alt="Modern educational facility" 
                  className="w-full h-auto object-cover transform transition-transform duration-700 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-gradient-to-b from-indigo-600/10 via-transparent to-indigo-600/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              </div>
            </div>

            {/* Content */}
            <div className="space-y-8 order-1 lg:order-2 animate-fade-in-up">
              <h2 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white leading-tight">
                The Real Cost of Manual Resource Management
              </h2>
              <div className="space-y-4">
                <p className="text-lg md:text-xl text-gray-700 dark:text-gray-300 leading-relaxed font-light">
                  When institutions rely on email chains, spreadsheets, and phone calls to coordinate facility bookings, the consequences ripple across the entire organization. Faculty members waste valuable preparation time searching for available spaces, administrative staff becomes trapped in a cycle of scheduling conflicts and confirmations.
                </p>
                <p className="text-lg md:text-xl text-gray-700 dark:text-gray-300 leading-relaxed font-light">
                  The problem isn't just inconvenience—it's an opportunity cost. Every minute spent managing room bookings manually is a minute not spent on education, research, or strategic planning.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section className="relative py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-slate-50 to-white dark:from-gray-800 dark:to-gray-900 overflow-hidden">
        <div className="w-full relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center max-w-7xl mx-auto">
            {/* Content */}
            <div className="space-y-8 animate-fade-in-up">
              <h2 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white leading-tight">
                A Platform Built for Real Institutional Needs
              </h2>
              <div className="space-y-4">
                <p className="text-lg md:text-xl text-gray-700 dark:text-gray-300 leading-relaxed font-light">
                  STONSET fundamentally changes how universities and colleges approach resource management. Instead of reactive firefighting, institutions gain proactive visibility into their entire facility ecosystem. Every booking is instantly confirmed, conflicts are automatically prevented before they happen.
                </p>
                <p className="text-lg md:text-xl text-gray-700 dark:text-gray-300 leading-relaxed font-light">
                  The platform works by replacing fragmented systems with a single source of truth. Faculty request a room and get immediate confirmation. Department heads see real-time availability. Administrators gain actionable insights into utilization patterns.
                </p>
              </div>
            </div>

            {/* Image */}
            <div className="hidden lg:block">
              <div className="group relative overflow-hidden rounded-3xl shadow-2xl transform transition-transform duration-500 hover:scale-105">
                <img 
                  src="/images/pexels-pavel-danilyuk-8423380.jpg" 
                  alt="Educational technology environment" 
                  className="w-full h-auto object-cover transform transition-transform duration-700 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-tl from-emerald-600/20 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why STONSET Section with Implicit Grid */}
      <section className="relative py-24 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-900 overflow-hidden">
        <div className="max-w-full mx-auto relative z-10 w-full">
          <div className="mb-16 text-center animate-fade-in">
            <h2 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
              Why Institutions Choose STONSET
            </h2>
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-400 font-light">
              Built by people who understand higher education operations
            </p>
          </div>

          {/* Implicit Grid Layout for Content */}
          <div className="grid auto-rows-max gap-8 md:gap-12 grid-cols-1 md:grid-cols-2 lg:grid-cols-4 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
            <div className="space-y-4 group">
              <h3 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
                It Actually Solves the Problem
              </h3>
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed font-light">
                STONSET doesn't just automate broken processes—it reimagines how scheduling works. By giving every stakeholder real-time visibility, the coordination nightmare disappears.
              </p>
            </div>

            <div className="space-y-4 group">
              <h3 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
                Seamless Integration
              </h3>
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed font-light">
                We understand your institution's existing systems. STONSET integrates with your infrastructure, respects your governance structure, and works with departments as they actually operate.
              </p>
            </div>

            <div className="space-y-4 group">
              <h3 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
                Data-Driven Insights
              </h3>
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed font-light">
                Stop guessing about facility utilization. STONSET gives you clear visibility into which resources are overextended, which are underused, and where to invest next.
              </p>
            </div>

            <div className="space-y-4 group">
              <h3 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
                Scales With You
              </h3>
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed font-light">
                Whether you manage three buildings or hundreds, STONSET adapts to your structure. Add facilities, expand departments, change workflows—the system grows with you.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Image Gallery with Implicit Grid */}
      <section className="relative py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-slate-50 to-white dark:from-gray-800 dark:to-gray-900 overflow-hidden">
        <div className="w-full relative z-10 max-w-full">
          <h2 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-16 text-center leading-tight">
            Modern Facility Management in Action
          </h2>
          
          {/* Implicit Grid for Images - Auto-fit with minimum width */}
          <div className="grid gap-6 md:gap-8 auto-cols-fr" style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gridAutoRows: 'auto',
            gap: '1.5rem'
          }}>
            <div className="group relative overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 h-80">
              <img 
                src="/images/realtime.jpg" 
                alt="Scheduling interface" 
                className="w-full h-full object-cover transform transition-transform duration-500 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <p className="absolute bottom-0 left-0 right-0 p-6 text-white font-light text-lg translate-y-6 group-hover:translate-y-0 transition-transform duration-300">Real-time Booking System</p>
            </div>

            <div className="group relative overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 h-80">
              <img 
                src="/images/oversight.jpg" 
                alt="Facility management" 
                className="w-full h-full object-cover transform transition-transform duration-500 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <p className="absolute bottom-0 left-0 right-0 p-6 text-white font-light text-lg translate-y-6 group-hover:translate-y-0 transition-transform duration-300">Facility Oversight</p>
            </div>

            <div className="group relative overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 h-80">
              <img 
                src="/images/unified.png" 
                alt="Technology platform" 
                className="w-full h-full object-cover transform transition-transform duration-500 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <p className="absolute bottom-0 left-0 right-0 p-6 text-white font-light text-lg translate-y-6 group-hover:translate-y-0 transition-transform duration-300">Unified Platform</p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="relative py-32 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-indigo-600 via-indigo-700 to-indigo-800 text-white overflow-hidden min-h-96 flex items-center">
        {/* Animated Background Blobs */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-10 right-20 w-64 h-64 bg-white rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
          <div className="absolute bottom-10 left-20 w-64 h-64 bg-indigo-200 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000"></div>
        </div>

        <div className="text-center relative z-10 w-full max-w-none px-4 sm:px-6 lg:px-8">
          <div className="space-y-8 animate-fade-in">
            <h2 className="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight">
              Ready to Transform Your Institution?
            </h2>
            <p className="text-xl md:text-2xl text-indigo-100 leading-relaxed font-light px-4">
              Stop fighting the scheduling system. Start seeing real-time visibility into your facility usage and eliminate double-bookings forever.
            </p>
          </div>

          <div className="mt-12 animate-fade-in-delay-3 flex flex-col sm:flex-row gap-4 justify-center px-4">
            {!isLoggedIn && (
              <>
                <Link to="/register">
                  <Button 
                    variant="ghost" 
                    size="lg" 
                    className="bg-white text-indigo-600 hover:bg-slate-100 font-semibold transform transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-white/30"
                  >
                    Try STONSET Free
                    <ArrowRight size={20} className="ml-2" />
                  </Button>
                </Link>
                <Link to="/login">
                  <Button 
                    variant="ghost" 
                    size="lg" 
                    className="border-2 border-white text-white hover:bg-indigo-700 font-semibold transform transition-all duration-300"
                  >
                    Sign In
                  </Button>
                </Link>
              </>
            )}
            {isLoggedIn && (
              <Link to="/dashboard">
                <Button 
                  variant="ghost" 
                  size="lg" 
                  className="bg-white text-indigo-600 hover:bg-slate-100 font-semibold transform transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-white/30"
                >
                  Go to Dashboard
                  <ArrowRight size={20} className="ml-2" />
                </Button>
              </Link>
            )}
          </div>
        </div>
      </section>
    </div>
  )
}

export { HomePage }
