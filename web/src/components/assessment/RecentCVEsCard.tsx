import { ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline'

interface CVE {
  cve_id: string
  severity: string | null
  description: string
  year: number
  sources: string[]
}

interface RecentCVEsCardProps {
  cves: CVE[]
}

const getSeverityColor = (severity: string | null) => {
  if (!severity) return 'text-gray-500 dark:text-gray-400'

  const severityLower = severity.toLowerCase()
  if (severityLower === 'critical') return 'text-red-600 dark:text-red-400'
  if (severityLower === 'high') return 'text-orange-600 dark:text-orange-400'
  if (severityLower === 'medium') return 'text-yellow-600 dark:text-yellow-400'
  if (severityLower === 'low') return 'text-green-600 dark:text-green-400'
  return 'text-gray-500 dark:text-gray-400'
}

export default function RecentCVEsCard({ cves }: RecentCVEsCardProps) {
  return (
    <div className="bg-white dark:bg-gray-700 rounded-2xl p-6 border border-gray-300 dark:border-gray-600 shadow-sm">
      <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 text-center">
        Recent CVEs
      </h4>

      {cves.length === 0 ? (
        <div className="flex items-center justify-center h-32">
          <p className="text-gray-500 dark:text-gray-400 text-center">
            No recent CVEs found
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {cves.map((cve, index) => (
            <div
              key={index}
              className="pb-4 border-b border-gray-200 dark:border-gray-600 last:border-b-0 last:pb-0"
            >
              <div className="flex items-center gap-2 mb-1">
                <span className="font-bold text-gray-900 dark:text-white">
                  {cve.cve_id}
                </span>
                {cve.sources.length > 0 && (
                  <a
                    href={cve.sources[0]}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300"
                    title="View CVE details"
                  >
                    <ArrowTopRightOnSquareIcon className="h-4 w-4" />
                  </a>
                )}
              </div>
              <p className={`text-sm ${getSeverityColor(cve.severity)}`}>
                {cve.severity || 'Unknown'} {cve.year && `(${cve.year})`}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
