import { useNavigate } from 'react-router-dom'
import { ShieldCheckIcon, DocumentMagnifyingGlassIcon, ChartBarIcon, ArrowRightIcon } from '@heroicons/react/24/outline'

export default function Home() {
  const navigate = useNavigate()

  const handleGetStarted = () => {
    navigate('/name')
  }

  return (
    <div className="animate-fade-in max-w-4xl mx-auto mt-32">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-6">
          AI-Powered Security Assessment
        </h1>
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

      <div className="mt-12 text-center text-sm text-gray-500 dark:text-gray-400">
        <p>Helping security teams move from reactive firefighting to proactive enablement</p>
      </div>
    </div>
  )
}
