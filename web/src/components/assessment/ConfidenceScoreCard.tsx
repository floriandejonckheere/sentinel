interface ConfidenceScoreCardProps {
  confidence: string
}

function getConfidenceText(confidence: string): string {
  if (confidence === 'low') return 'Low'
  if (confidence === 'medium') return 'Medium'
  if (confidence === 'high') return 'High'
  return confidence
}

function getConfidenceColor(confidence: string): string {
  if (confidence === 'low') return 'text-red-600 dark:text-red-400'
  if (confidence === 'medium') return 'text-orange-600 dark:text-orange-400'
  if (confidence === 'high') return 'text-green-600 dark:text-green-400'
  return 'text-gray-600 dark:text-gray-400'
}

export default function ConfidenceScoreCard({ confidence }: ConfidenceScoreCardProps) {
  return (
    <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600 shadow-lg">
      <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 text-center">
        Confidence Score
      </h4>

      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className={`text-7xl font-bold ${getConfidenceColor(confidence)}`}>
            {getConfidenceText(confidence)}
          </div>
          <p className="text-gray-500 dark:text-gray-400 mt-4">
            Assessment Confidence
          </p>
        </div>
      </div>
    </div>
  )
}
