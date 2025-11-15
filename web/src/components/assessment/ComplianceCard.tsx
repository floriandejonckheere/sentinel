import { ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline'

interface Framework {
    name: string
    compliance_level: "compliant" | "non-compliant" | "partial"
    last_audit_date: string
    url: string
    sources: string[]
}

interface ComplianceCardProps {
    frameworks: Framework[]
    data_residency: string[]
}

export default function ComplianceCard({frameworks, data_residency}: ComplianceCardProps) {
    const getComplianceLevelColor = (level: string) => {
        if (level === 'compliant') return 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30'
        if (level === 'non-compliant') return 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30'
        if (level === 'partial') return 'text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-900/30'
        return 'text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-900/30'
    }

    const formatComplianceLevel = (level: string) => {
        if (level === 'compliant') return 'Compliant'
        if (level === 'non-compliant') return 'Non-Compliant'
        if (level === 'partial') return 'Partial'
        return level
    }

    const formatDate = (date: string) => {
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

    return (
        <div
            className="bg-white dark:bg-gray-700 rounded-2xl p-6 border border-gray-300 dark:border-gray-600 shadow-sm">
            <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 text-center">
                Compliance
            </h4>

            {/* Data Residency Section */}
            <div className="mb-6">
                <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    Data Residency
                </h5>
                <div className="flex flex-wrap gap-2">
                    {data_residency.length === 0 ? (
                        <p className="text-gray-500 dark:text-gray-400 text-xs">
                            No data residency information available
                        </p>
                    ) : (
                        data_residency.map((location, index) => (
                            <span
                                key={index}
                                className="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full text-xs font-medium"
                            >
                                {location}
                            </span>
                        ))
                    )}
                </div>
            </div>

            {/* Compliance Frameworks Section */}
            <div>
                <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    Compliance Frameworks
                </h5>
                <div className="space-y-3">
                    {frameworks.length === 0 ? (
                        <p className="text-gray-500 dark:text-gray-400 text-xs">
                            No compliance frameworks available
                        </p>
                    ) : (
                        frameworks.map((framework, index) => (
                            <div key={index}
                                 className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-600">
                                <div className="flex items-start justify-between mb-2">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2">
                                            <h6 className="font-bold text-gray-900 dark:text-white text-sm">
                                                {framework.name}
                                            </h6>
                                            {framework.sources && framework.sources.length > 0 && (
                                                <div className="flex gap-1">
                                                    {framework.sources.map((source, idx) => (
                                                        <a
                                                            key={idx}
                                                            href={source}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300"
                                                            title={`Source ${idx + 1}: ${source}`}
                                                        >
                                                            <ArrowTopRightOnSquareIcon className="h-4 w-4" />
                                                        </a>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                    <span
                                        className={`px-2 py-1 rounded text-xs font-medium ${getComplianceLevelColor(framework.compliance_level)}`}>
                                        {formatComplianceLevel(framework.compliance_level)}
                                    </span>
                                </div>

                                {framework.last_audit_date && (
                                    <div className="text-xs text-gray-600 dark:text-gray-400">
                                        <span className="font-semibold">Last audit:</span> {formatDate(framework.last_audit_date)}
                                    </div>
                                )}
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    )
}
