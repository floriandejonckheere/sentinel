import { useNavigate } from 'react-router-dom'
import { ShieldCheckIcon, DocumentMagnifyingGlassIcon, ChartBarIcon, ArrowRightIcon } from '@heroicons/react/24/outline'
import { useEffect, useState } from 'react'

export default function Home() {
  const navigate = useNavigate()
  const [typedText, setTypedText] = useState('')
  const brand = 'Sentinel AI'

  useEffect(() => {
    let i = 0
    const interval = setInterval(() => {
      setTypedText(brand.slice(0, i + 1))
      i++
      if (i === brand.length) {
        clearInterval(interval)
      }
    }, 120)
    return () => clearInterval(interval)
  }, [])

  const handleGetStarted = () => {
    navigate('/name')
  }

  return (
    <div className="animate-fade-in max-w-4xl mx-auto mt-20">
      {/* Branding Banner */}
      <div className="flex flex-col items-center mb-20">
        <div className="flex items-center gap-6">
          <div className="relative">
            <ShieldCheckIcon className="h-24 w-24 text-blue-600 dark:text-blue-400 drop-shadow-lg" />
          </div>
          <h1 className="text-7xl font-light tracking-tight text-gray-900 dark:text-white leading-none">
            <span className="inline-block">
              {typedText}
              {/* Baseline-aligned blinking cursor (smaller, like lowercase 'l') */}
              <span className="ml-1 inline-block w-[0.06em] h-[0.8em] bg-blue-600 dark:bg-blue-400 animate-pulse align-baseline" />
            </span>
          </h1>
        </div>
        <p className="mt-8 text-xl text-gray-600 dark:text-gray-300 max-w-2xl text-center">
          AI-Powered Security Assessment Platform
        </p>
      </div>

      <div className="text-center mb-12">
        <h2 className="text-5xl font-bold text-gray-900 dark:text-white mb-6">
          AI-Powered Security Assessment
        </h2>
        <p className="text-xl text-gray-700 dark:text-gray-300 mb-8">
          Transform business decisions into CISO-ready trust briefs in minutes
        </p>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
          Sentinel is an AI-powered security assessor that evaluates IT tools and provides comprehensive,
          source-grounded analysis including CVE trends, compliance signals, risk scoring, and safer alternatives.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8 mb-12">
        <div className="bg-white dark:bg-gray-700 rounded-2xl p-6 border border-gray-300 dark:border-gray-600">
          <DocumentMagnifyingGlassIcon className="h-12 w-12 text-blue-600 dark:text-blue-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
            Source-Grounded Analysis
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Fetch reliable signals from vendor security pages, CVE databases, CISA KEV, and compliance attestations with full citations.
          </p>
        </div>

        <div className="bg-white dark:bg-gray-700 rounded-2xl p-6 border border-gray-300 dark:border-gray-600">
          <ChartBarIcon className="h-12 w-12 text-blue-600 dark:text-blue-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
            Comprehensive Scoring
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Get transparent 0-100 trust scores with detailed rationale covering security posture, incidents, and data handling.
          </p>
        </div>

        <div className="bg-white dark:bg-gray-700 rounded-2xl p-6 border border-gray-300 dark:border-gray-600">
          <ShieldCheckIcon className="h-12 w-12 text-blue-600 dark:text-blue-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
            Safer Alternatives
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Discover 1-2 safer alternatives with clear rationale to help you make informed security decisions.
          </p>
        </div>
      </div>

      <div className="text-center">
        <button
          onClick={handleGetStarted}
          className="inline-flex items-center gap-3 px-8 py-4 bg-blue-600 dark:bg-blue-500 hover:bg-blue-700 dark:hover:bg-blue-600 text-white text-lg font-semibold rounded-2xl shadow-lg hover:shadow-xl transition-all"
        >
          Start Assessment
          <ArrowRightIcon className="h-6 w-6" />
        </button>
      </div>
    </div>
  )
}
