interface ArchitectureCardProps {
    architecture: {
        encryption: string
        key_derivation: string
        zero_knowledge: boolean
        open_source: boolean
        authentication: string
        deployment: "on-premise" | "cloud" | "saas" | "hybrid"
    }
}

export default function ArchitectureCard({architecture}: ArchitectureCardProps) {
    const formatDeployment = (deployment: string) => {
        if (deployment === 'on-premise') return 'On-Premise'
        if (deployment === 'cloud') return 'Cloud'
        if (deployment === 'saas') return 'SaaS'
        if (deployment === 'hybrid') return 'Hybrid'
        return deployment
    }

    const formatBoolean = (value: boolean) => {
        return value ? 'Yes' : 'No'
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
                    <span className="text-gray-700 dark:text-gray-300">{formatDeployment(architecture.deployment)}</span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Open source:</span>
                    <span className="text-gray-700 dark:text-gray-300">{formatBoolean(architecture.open_source)}</span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Zero knowledge:</span>
                    <span className="text-gray-700 dark:text-gray-300">{formatBoolean(architecture.zero_knowledge)}</span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Authentication:</span>
                    <span className="text-gray-700 dark:text-gray-300">{architecture.authentication}</span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Encryption:</span>
                    <span className="text-gray-700 dark:text-gray-300">{architecture.encryption}</span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900 dark:text-white">Key derivation:</span>
                    <span className="text-gray-700 dark:text-gray-300">{architecture.key_derivation}</span>
                </div>
            </div>
        </div>
    )
}
