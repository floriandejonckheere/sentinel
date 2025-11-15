interface TrustScoreCardProps {
  score: number
}

function getTrustScoreColor(score: number): string {
  if (score < 50) return 'text-red-600 dark:text-red-400'
  if (score < 75) return 'text-orange-600 dark:text-orange-400'
  if (score < 90) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-green-600 dark:text-green-400'
}

function getTrustScoreStrokeColor(score: number): string {
  if (score < 50) return '#dc2626'
  if (score < 75) return '#ea580c'
  if (score < 90) return '#ca8a04'
  return '#16a34a'
}

export default function TrustScoreCard({ score }: TrustScoreCardProps) {
  return (
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
              stroke={getTrustScoreStrokeColor(score)}
              strokeWidth="20"
              fill="none"
              strokeDasharray={`${(score / 100) * 502.65} 502.65`}
              strokeLinecap="round"
              className="transition-all duration-1000 ease-out"
            />
          </svg>

          {/* Score text in center */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className={`text-5xl font-bold ${getTrustScoreColor(score)}`}>
                {score}
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400">out of 100</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
