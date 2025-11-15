import React from "react";

interface KeyTakeawaysCardProps {
    strengths: string[]
    risks: string[]
}

export default function KeyTakeawaysCard({strengths, risks}: KeyTakeawaysCardProps) {
    return (
        <div
            className="bg-white dark:bg-gray-700 rounded-2xl p-6 border border-gray-300 dark:border-gray-600 shadow-sm h-full">
            <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 text-center">
              Key takeaways
            </h4>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Key Strengths Column */}
                <div>
                    <h4 className="text-lg font-medium text-green-600 dark:text-green-400 mb-4">
                        Key Strengths
                    </h4>
                    <ul className="space-y-2">
                        {strengths.map((strength, index) => (
                            <li key={index} className="flex items-start">
                                <span
                                    className="text-green-500 dark:text-green-400 mr-2 flex-shrink-0 mt-1">✓</span>
                                <span className="text-gray-700 dark:text-gray-300">{strength}</span>
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Key Risks Column */}
                <div>
                    <h4 className="text-lg font-medium text-red-600 dark:text-red-400 mb-4">
                        Key Risks
                    </h4>
                    <ul className="space-y-2">
                        {risks.map((risk, index) => (
                            <li key={index} className="flex items-start">
                                <span
                                    className="text-red-500 dark:text-red-400 mr-2 flex-shrink-0 mt-1">⚠</span>
                                <span className="text-gray-700 dark:text-gray-300">{risk}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

            {/* Explanation */}
            <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-600">
                <p className="text-xs text-gray-600 dark:text-gray-400 text-justify">
                    Key takeaways are identified through AI-powered analysis of security documentation, vulnerability databases, compliance certifications, and industry best practices to highlight the most critical strengths and risks.
                </p>
            </div>
        </div>
    )
}
