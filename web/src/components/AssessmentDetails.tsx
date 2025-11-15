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

  return (
    <div className="animate-fade-in text-center w-full max-w-3xl">
      <h2 className="text-3xl font-medium text-gray-900 dark:text-white mb-6">
        Assessment Complete
      </h2>
      <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600 space-y-6">
        <div className="border-b border-gray-200 dark:border-gray-600 pb-6">
          <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
            {assessment.application.name}
          </h3>
          <p className="text-gray-600 dark:text-gray-400">{assessment.application.description}</p>
        </div>

        <div className="grid grid-cols-2 gap-4 text-left">
          <div>
            <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Vendor</span>
            <span className="text-lg text-gray-900 dark:text-white">{assessment.vendor.name}</span>
          </div>
          <div>
            <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Category</span>
            <span className="text-lg text-gray-900 dark:text-white">{assessment.application.category}</span>
          </div>
          <div>
            <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Trust Score</span>
            <span className="text-2xl font-bold text-green-600 dark:text-green-400">{assessment.trust_score}/100</span>
          </div>
          <div>
            <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Confidence</span>
            <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">{assessment.confidence}%</span>
          </div>
        </div>
      </div>
    </div>
  )
}
