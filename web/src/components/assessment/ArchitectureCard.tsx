interface ArchitectureCardProps {
    architecture: {
        encryption: string | null
        key_derivation: string | null
        zero_knowledge: boolean | null
        open_source: boolean | null
        authentication: string | null
        deployment: "on-premise" | "cloud" | "saas" | "hybrid" | null
    }
}

export default function ArchitectureCard({architecture}: ArchitectureCardProps) {
    const formatDeployment = (deployment: string | null) => {
        if (!deployment) return 'Unknown'
        if (deployment === 'on-premise') return 'On-Premise'
        if (deployment === 'cloud') return 'Cloud'
        if (deployment === 'saas') return 'SaaS'
        if (deployment === 'hybrid') return 'Hybrid'
        return deployment
    }

    const formatBoolean = (value: boolean | null) => {
        if (value === null) return 'Unknown'
        return value ? 'Yes' : 'No'
    }

    const formatString = (value: string | null) => {
        return value || 'Unknown'
    }

    return (
        <div
            className="bg-white dark:bg-gray-700 rounded-2xl p-6 border border-gray-300 dark:border-gray-600 shadow-sm h-full">
            <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 text-center">
                Architecture
            </h4>

            <div className="space-y-3">
                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Deployment model:</span>
                    <span className={architecture.deployment ? "text-gray-700 dark:text-gray-300" : "text-gray-400 dark:text-gray-500"}>
                        {formatDeployment(architecture.deployment)}
                    </span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Open source:</span>
                    <span className={architecture.open_source !== null ? "text-gray-700 dark:text-gray-300" : "text-gray-400 dark:text-gray-500"}>
                        {formatBoolean(architecture.open_source)}
                    </span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Zero knowledge:</span>
                    <span className={architecture.zero_knowledge !== null ? "text-gray-700 dark:text-gray-300" : "text-gray-400 dark:text-gray-500"}>
                        {formatBoolean(architecture.zero_knowledge)}
                    </span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Authentication:</span>
                    <span className={architecture.authentication ? "text-gray-700 dark:text-gray-300" : "text-gray-400 dark:text-gray-500"}>
                        {formatString(architecture.authentication)}
                    </span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Encryption:</span>
                    <span className={architecture.encryption ? "text-gray-700 dark:text-gray-300" : "text-gray-400 dark:text-gray-500"}>
                        {formatString(architecture.encryption)}
                    </span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Key derivation:</span>
                    <span className={architecture.key_derivation ? "text-gray-700 dark:text-gray-300" : "text-gray-400 dark:text-gray-500"}>
                        {formatString(architecture.key_derivation)}
                    </span>
                </div>
            </div>
        </div>
    )
}
