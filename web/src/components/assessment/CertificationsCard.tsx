interface Certification {
    name: string
    status: "active" | "expired" | "pending"
    issued_by: string
    issue_date: string
    expiry_date: string
    url: string
}

interface CertificationsCardProps {
    certs: Certification[]
}

export default function CertificationsCard({certs}: CertificationsCardProps) {
    const getStatusColor = (status: string) => {
        if (status === 'active') return 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30'
        if (status === 'expired') return 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30'
        if (status === 'pending') return 'text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-900/30'
        return 'text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-900/30'
    }

    const formatStatus = (status: string) => {
        return status.charAt(0).toUpperCase() + status.slice(1)
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
                Certifications
            </h4>

            <div className="space-y-4">
                {certs.length === 0 ? (
                    <p className="text-gray-500 dark:text-gray-400 text-center text-sm">
                        No certifications available
                    </p>
                ) : (
                    certs.map((cert, index) => (
                        <div key={index}
                             className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-600">
                            <div className="flex items-start justify-between mb-2">
                                <div className="flex-1">
                                    <h5 className="font-bold text-gray-900 dark:text-white mb-1">
                                        {cert.name}
                                        {cert.url && (
                                            <a
                                                href={cert.url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="ml-2 text-blue-600 dark:text-blue-400 hover:underline text-xs"
                                                title="View certification"
                                            >
                                                ↗
                                            </a>
                                        )}
                                    </h5>
                                </div>
                                <span
                                    className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(cert.status)}`}>
                                    {formatStatus(cert.status)}
                                </span>
                            </div>

                            <div className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                                {cert.issued_by && (
                                    <div>
                                        <span className="font-semibold">Issued by:</span> {cert.issued_by}
                                    </div>
                                )}
                                {cert.issue_date && (
                                    <div>
                                        <span className="font-semibold">Issue date:</span> {formatDate(cert.issue_date)}
                                    </div>
                                )}
                                {cert.expiry_date && (
                                    <div>
                                        <span className="font-semibold">Expiry date:</span> {formatDate(cert.expiry_date)}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    )
}
