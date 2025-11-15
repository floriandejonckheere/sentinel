import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline'
import { createAssessment } from '../../services/api'

interface AlternativesCardProps {
  alternatives: {
    name: string
    reason: string
  }[]
  currentRole?: string
}

export default function AlternativesCard({ alternatives, currentRole = 'global' }: AlternativesCardProps) {
  const navigate = useNavigate()
  const [loadingIndex, setLoadingIndex] = useState<number | null>(null)

  const handleAlternativeClick = async (alternativeName: string, index: number) => {
    setLoadingIndex(index)

    try {
      const assessmentId = await createAssessment({
        name: alternativeName,
        role: currentRole,
        size: 'medium', // Default value
        risk: 'medium', // Default value
      })

      // Navigate to the new assessment details page with role query param
      const roleParam = currentRole ? `?role=${encodeURIComponent(currentRole)}` : ''
      navigate(`/assessments/${assessmentId}${roleParam}`)
    } catch (error) {
      console.error('Failed to create assessment:', error)
      setLoadingIndex(null)
    }
  }

  return (
    <div className="bg-white dark:bg-gray-700 rounded-2xl p-6 border border-gray-300 dark:border-gray-600 shadow-sm h-full">
      <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 text-center">
        Alternatives
      </h4>

      {alternatives.length === 0 ? (
        <div className="flex items-center justify-center h-32">
          <p className="text-gray-500 dark:text-gray-400 text-center">
            No alternatives available
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {alternatives.map((alternative, index) => (
            <div key={index} className="pb-4 border-b border-gray-200 dark:border-gray-600 last:border-b-0 last:pb-0">
              <div className="flex items-center gap-2 mb-1">
                <button
                  onClick={() => handleAlternativeClick(alternative.name, index)}
                  disabled={loadingIndex === index}
                  className="font-bold text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 hover:underline text-left disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
                >
                  {alternative.name}
                  {loadingIndex === index ? (
                    <span className="animate-spin inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full" />
                  ) : null}
                </button>
              </div>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {alternative.reason}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
