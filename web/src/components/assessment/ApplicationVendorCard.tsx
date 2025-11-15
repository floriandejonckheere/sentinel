interface ApplicationVendorCardProps {
  application: {
    application_intel: {
        name: string
        vendor_name: string
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
    url: string
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
    <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600 shadow-lg relative">
      <div className="absolute top-4 right-6">
        <p className="text-xs text-gray-500 dark:text-gray-400" title={formatDate(assessedAt)}>
          Assessed <span className="cursor-help">{getRelativeTime(assessedAt)}</span>
        </p>
      </div>

      <h3 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
        {application.application_intel.name}
      </h3>
      <p className="text-xl text-gray-600 dark:text-gray-400 mb-6">
        By {application.application_intel.vendor_name}{vendor.country ? `, ${getCountryName(vendor.country)}` : ''}
      </p>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-left pt-6 border-t border-gray-200 dark:border-gray-600">
        <div>
          <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
            Category
          </span>
          <span className="text-base text-gray-900 dark:text-white">
            {application.category}
          </span>
        </div>
        <div>
          <span className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
            Subcategory
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
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
        <p className="text-gray-600 dark:text-gray-400">
          {application.description}
        </p>
      </div>
    </div>
  )
}
