import { ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline'

interface Incident {
  title: string
  date: string | null
  severity: "High" | "Medium" | "Low" | null
  description: string
  sources: string[]
}

interface RecentIncidentsCardProps {
  incidents: Incident[]
}

const getSeverityColor = (severity: string | null) => {
  if (!severity) return 'text-gray-500 dark:text-gray-400'

  const severityLower = severity.toLowerCase()
  if (severityLower === 'high') return 'text-red-600 dark:text-red-400'
  if (severityLower === 'medium') return 'text-orange-600 dark:text-orange-400'
  if (severityLower === 'low') return 'text-yellow-600 dark:text-yellow-400'
  return 'text-gray-500 dark:text-gray-400'
}

const formatDate = (date: string | null) => {
  if (!date) return null
  try {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return date
  }
}

export default function RecentIncidentsCard({ incidents }: RecentIncidentsCardProps) {
  return (
    <div className="bg-white dark:bg-gray-700 rounded-2xl p-6 border border-gray-300 dark:border-gray-600 shadow-sm">
      <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 text-center">
        Recent Incidents
      </h4>

      {incidents.length === 0 ? (
        <div className="flex items-center justify-center h-32">
          <p className="text-gray-500 dark:text-gray-400 text-center">
            No recent incidents found
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {incidents.map((incident, index) => (
            <div
              key={index}
              className="pb-4 border-b border-gray-200 dark:border-gray-600 last:border-b-0 last:pb-0"
            >
              <div className="flex items-center gap-2 mb-1">
                <span className="font-bold text-gray-900 dark:text-white">
                  {incident.title}
                </span>
                {incident.sources.length > 0 && (
                  <a
                    href={incident.sources[0]}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300"
                    title="View incident details"
                  >
                    <ArrowTopRightOnSquareIcon className="h-4 w-4" />
                  </a>
                )}
              </div>
              <p className={`text-sm ${getSeverityColor(incident.severity)}`}>
                {incident.severity || 'Unknown severity'} {incident.date && `• ${formatDate(incident.date)}`}
              </p>
              {incident.description && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                  {incident.description}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
