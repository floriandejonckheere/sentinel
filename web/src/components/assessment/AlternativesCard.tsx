interface AlternativesCardProps {
  alternatives: {
    name: string
    reason: string
  }[]
}

export default function AlternativesCard({ alternatives }: AlternativesCardProps) {
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
              <p className="font-bold text-gray-900 dark:text-white mb-1">
                {alternative.name}
              </p>
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
