import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { getAssessment, type Assessment } from '../services/api'
import LoadingSpinner from './LoadingSpinner'

export default function AssessmentDetails() {
  const { id } = useParams<{ id: string }>()
  const [isLoading, setIsLoading] = useState(true)
  const [assessment, setAssessment] = useState<Assessment | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (id) {
      fetchAssessment(id)
    }
  }, [id])

  const fetchAssessment = async (assessmentId: string) => {
    setIsLoading(true)
    setError(null)

    try {
      const fetchedAssessment = await getAssessment(assessmentId)
      setAssessment(fetchedAssessment)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return <LoadingSpinner message="Loading assessment..." />
  }

  if (error) {
    return (
      <div className="animate-fade-in text-center w-full max-w-3xl">
        <div className="bg-red-50 dark:bg-red-900/20 rounded-2xl p-8 border border-red-300 dark:border-red-600">
          <h2 className="text-2xl font-medium text-red-900 dark:text-red-200 mb-4">
            Error
          </h2>
          <p className="text-red-700 dark:text-red-300">{error}</p>
        </div>
      </div>
    )
  }

  if (!assessment) {
    return (
      <div className="animate-fade-in text-center w-full max-w-3xl">
        <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600">
          <p className="text-gray-700 dark:text-gray-300">Assessment not found</p>
        </div>
      </div>
    )
  }

  const getTrustScoreColor = (score: number): string => {
    if (score < 50) return 'text-red-600 dark:text-red-400'
    if (score < 75) return 'text-orange-600 dark:text-orange-400'
    if (score < 90) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-green-600 dark:text-green-400'
  }

  const getTrustScoreStrokeColor = (score: number): string => {
    if (score < 50) return '#dc2626'
    if (score < 75) return '#ea580c'
    if (score < 90) return '#ca8a04'
    return '#16a34a'
  }

  const getConfidenceText = (confidence: string): string => {
    if (confidence === 'low') return 'Low'
    if (confidence === 'medium') return 'Medium'
    if (confidence === 'high') return 'High'
    return confidence
  }

  const getConfidenceColor = (confidence: string): string => {
    if (confidence === 'low') return 'text-red-600 dark:text-red-400'
    if (confidence === 'medium') return 'text-orange-600 dark:text-orange-400'
    if (confidence === 'high') return 'text-green-600 dark:text-green-400'
    return 'text-gray-600 dark:text-gray-400'
  }

  const getCountryName = (countryCode: string): string => {
    const countryMap: Record<string, string> = {
      'US': 'United States',
      'GB': 'United Kingdom',
      'UK': 'United Kingdom',
      'CA': 'Canada',
      'AU': 'Australia',
      'DE': 'Germany',
      'FR': 'France',
      'IT': 'Italy',
      'ES': 'Spain',
      'NL': 'Netherlands',
      'BE': 'Belgium',
      'SE': 'Sweden',
      'NO': 'Norway',
      'DK': 'Denmark',
      'FI': 'Finland',
      'IE': 'Ireland',
      'CH': 'Switzerland',
      'AT': 'Austria',
      'PL': 'Poland',
      'CZ': 'Czech Republic',
      'IN': 'India',
      'CN': 'China',
      'JP': 'Japan',
      'KR': 'South Korea',
      'SG': 'Singapore',
      'HK': 'Hong Kong',
      'IL': 'Israel',
      'BR': 'Brazil',
      'MX': 'Mexico',
      'AR': 'Argentina',
      'NZ': 'New Zealand',
      'ZA': 'South Africa',
    }
    return countryMap[countryCode.toUpperCase()] || countryCode
  }

  return (
    <div className="animate-fade-in w-full max-w-5xl px-4">
      <h2 className="text-3xl font-medium text-gray-900 dark:text-white mb-6 text-center">
        Assessment Complete
      </h2>

      {/* First Row - Application & Vendor Card */}
      <div className="mb-6">
        <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600 shadow-lg">
          <h3 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
            {assessment.application.name}
          </h3>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-6">
            By {assessment.vendor.name}, {getCountryName(assessment.vendor.country)}
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-left pt-6 border-t border-gray-200 dark:border-gray-600">
            <div>
              <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                Category
              </span>
              <span className="text-base text-gray-900 dark:text-white">
                {assessment.application.category}
              </span>
            </div>
            <div>
              <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                Subcategory
              </span>
              <span className="text-base text-gray-900 dark:text-white">
                {assessment.application.subcategory}
              </span>
            </div>
            <div>
              <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                Legal Name
              </span>
              <span className="text-base text-gray-900 dark:text-white">
                {assessment.vendor.legal_name}
              </span>
            </div>
            <div>
              <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                Website
              </span>
              <a
                href={assessment.vendor.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-base text-blue-600 dark:text-blue-400 hover:underline"
              >
                Visit
              </a>
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
            <p className="text-gray-600 dark:text-gray-400">
              {assessment.application.description}
            </p>
          </div>
        </div>
      </div>

      {/* Second Row - Trust Score & Confidence Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Trust Score Gauge Card */}
        <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600 shadow-lg">
          <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 text-center">
            Trust Score
          </h4>

          <div className="flex flex-col items-center justify-center">
            {/* Circular Gauge */}
            <div className="relative w-48 h-48 mb-4">
              {/* Background circle */}
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 200 200">
                <circle
                  cx="100"
                  cy="100"
                  r="80"
                  stroke="currentColor"
                  strokeWidth="20"
                  fill="none"
                  className="text-gray-200 dark:text-gray-600"
                />
                {/* Progress circle */}
                <circle
                  cx="100"
                  cy="100"
                  r="80"
                  stroke={getTrustScoreStrokeColor(assessment.trust_score)}
                  strokeWidth="20"
                  fill="none"
                  strokeDasharray={`${(assessment.trust_score / 100) * 502.65} 502.65`}
                  strokeLinecap="round"
                  className="transition-all duration-1000 ease-out"
                />
              </svg>

              {/* Score text in center */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className={`text-5xl font-bold ${getTrustScoreColor(assessment.trust_score)}`}>
                    {assessment.trust_score}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">out of 100</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Confidence Score Card */}
        <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600 shadow-lg">
          <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 text-center">
            Confidence Score
          </h4>

          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className={`text-7xl font-bold ${getConfidenceColor(assessment.confidence)}`}>
                {getConfidenceText(assessment.confidence)}
              </div>
              <p className="text-gray-500 dark:text-gray-400 mt-4">
                Assessment Confidence
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
