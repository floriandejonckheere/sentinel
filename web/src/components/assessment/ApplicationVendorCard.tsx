import { InformationCircleIcon } from '@heroicons/react/24/outline'

interface ApplicationVendorCardProps {
  application: {
    application_intel: {
        name: string
        vendor_name: string
        version: string | null
    }
    description: string
    url: string
    category: string
    subcategory: string
  }
  vendor: {
    name: string
    legal_name: string
    country: string | null
    url: string | null
    sources: string[]
  }
  assessedAt: string
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getRelativeTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  const diffWeeks = Math.floor(diffDays / 7)
  const diffMonths = Math.floor(diffDays / 30)
  const diffYears = Math.floor(diffDays / 365)

  if (diffMins < 1) return 'just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins === 1 ? '' : 's'} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours === 1 ? '' : 's'} ago`
  if (diffDays === 1) return 'yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffWeeks === 1) return 'last week'
  if (diffWeeks < 4) return `${diffWeeks} weeks ago`
  if (diffMonths === 1) return 'last month'
  if (diffMonths < 12) return `${diffMonths} months ago`
  if (diffYears === 1) return 'last year'
  return `${diffYears} years ago`
}

function getCountryName(countryCode?: string | null): string {
  if (!countryCode) return ''
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

export default function ApplicationVendorCard({ application, vendor, assessedAt }: ApplicationVendorCardProps) {
  return (
    <div className="bg-white dark:bg-gray-700 rounded-2xl p-4 sm:p-6 md:p-8 border border-gray-300 dark:border-gray-600 shadow-lg relative">
      <div className="absolute top-4 right-6">
        <p className="text-xs text-gray-500 dark:text-gray-400" title={formatDate(assessedAt)}>
          Assessed <span className="cursor-help">{getRelativeTime(assessedAt)}</span>
        </p>
      </div>

      <div className="mb-3">
        <h3 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 dark:text-white inline">
          {application.application_intel.name}
        </h3>
        {application.application_intel.version && (
          <span className="ml-2 sm:ml-3 text-sm sm:text-base md:text-lg text-gray-500 dark:text-gray-400">
            {application.application_intel.version}
          </span>
        )}
      </div>
      <p className="text-base sm:text-lg md:text-xl text-gray-600 dark:text-gray-400 mb-6">
        By {application.application_intel.vendor_name}{vendor.country ? ` (${getCountryName(vendor.country)})` : ''}
      </p>

      <div className={`grid ${vendor.url ? 'grid-cols-1 sm:grid-cols-2 md:grid-cols-4' : 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3'} gap-4 text-left pt-6 border-t border-gray-200 dark:border-gray-600`}>
        <div>
          <span className="flex items-center gap-1 text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
            Category
            <InformationCircleIcon
              className="h-4 w-4 text-gray-400 dark:text-gray-500 cursor-help"
              title="These (sub-)categories follow Gartner Market Guide, G2, Microsoft Enterprise, and NIST software function classes."
            />
          </span>
          <span className="text-base text-gray-900 dark:text-white">
            {application.category}
          </span>
        </div>
        <div>
          <span className="flex items-center gap-1 text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
            Subcategory
            <InformationCircleIcon
              className="h-4 w-4 text-gray-400 dark:text-gray-500 cursor-help"
              title="These (sub-)categories follow Gartner Market Guide, G2, Microsoft Enterprise, and NIST software function classes."
            />
          </span>
          <span className="text-base text-gray-900 dark:text-white">
            {application.subcategory}
          </span>
        </div>
        <div>
          <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
            Legal Name
          </span>
          <span className="text-base text-gray-900 dark:text-white">
            {vendor.legal_name}
          </span>
        </div>
        {vendor.url && (
          <div>
            <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
              Website
            </span>
            <a
              href={vendor.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-base text-blue-600 dark:text-blue-400 hover:underline"
            >
              Visit
            </a>
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
        <p className="text-gray-600 dark:text-gray-400">
          {application.description}
        </p>
      </div>

      {vendor.sources && vendor.sources.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-4">
            <h5 className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
              Sources & References
            </h5>
          </div>
          <div className="grid grid-cols-1 gap-2">
            {vendor.sources.map((source, index) => {
              const url = new URL(source)
              const domain = url.hostname.replace('www.', '')
              return (
                <a
                  key={index}
                  href={source}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group flex items-start gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/10 transition-all duration-200"
                >
                  <span className="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-xs font-semibold">
                    {index + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-medium text-gray-700 dark:text-gray-300 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                      {domain}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-500 truncate mt-0.5">
                      {source}
                    </div>
                  </div>
                  <svg
                    className="flex-shrink-0 w-4 h-4 text-gray-400 dark:text-gray-500 group-hover:text-blue-600 dark:group-hover:text-blue-400 transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
