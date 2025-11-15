interface SpiderChartCardProps {
    data: {
        architecture: number
        data_protection: number
        identity_access: number
        devsecops: number
        historical_security: number
        compliance: number
        platform_security: number
        risks_exposure: number
    }
}

interface DataPoint {
    label: string
    value: number
    key: string
}

function polarToCartesian(centerX: number, centerY: number, radius: number, angleInDegrees: number) {
    const angleInRadians = ((angleInDegrees - 90) * Math.PI) / 180.0
    return {
        x: centerX + radius * Math.cos(angleInRadians),
        y: centerY + radius * Math.sin(angleInRadians),
    }
}

export default function SpiderChartCard({data}: SpiderChartCardProps) {
    const centerX = 180
    const centerY = 180
    const maxRadius = 100
    const levels = 5

    const dataPoints: DataPoint[] = [
        {label: 'Architecture', value: data.architecture, key: 'architecture'},
        {label: 'Data Protection', value: data.data_protection, key: 'data_protection'},
        {label: 'Identity & Access', value: data.identity_access, key: 'identity_access'},
        {label: 'DevSecOps', value: data.devsecops, key: 'devsecops'},
        {label: 'Historical Security', value: data.historical_security, key: 'historical_security'},
        {label: 'Compliance', value: data.compliance, key: 'compliance'},
        {label: 'Platform Security', value: data.platform_security, key: 'platform_security'},
        {label: 'Risk Exposure', value: data.risks_exposure, key: 'risks_exposure'},
    ]

    const numPoints = dataPoints.length
    const angleStep = 360 / numPoints

    // Generate grid levels
    const gridLevels = Array.from({length: levels}, (_, i) => {
        const radius = (maxRadius / levels) * (i + 1)
        const points = Array.from({length: numPoints}, (_, j) => {
            const angle = j * angleStep
            return polarToCartesian(centerX, centerY, radius, angle)
        })
        return points
    })

    // Generate data polygon points
    const dataPolygonPoints = dataPoints.map((point, i) => {
        const angle = i * angleStep
        const radius = (point.value / 100) * maxRadius
        return polarToCartesian(centerX, centerY, radius, angle)
    })

    return (
        <div
            className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600 shadow-lg">
            <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 text-center">
                Trust Score Breakdown
            </h4>

            <div className="flex justify-center">
                <svg width="400" height="320" viewBox="0 0 360 360">
                    {/* Grid levels */}
                    {gridLevels.map((points, levelIndex) => (
                        <polygon
                            key={`level-${levelIndex}`}
                            points={points.map(p => `${p.x},${p.y}`).join(' ')}
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1"
                            className="stroke-gray-300 dark:stroke-gray-600"
                        />
                    ))}

                    {/* Axis lines */}
                    {dataPoints.map((_, i) => {
                        const angle = i * angleStep
                        const point = polarToCartesian(centerX, centerY, maxRadius, angle)
                        return (
                            <line
                                key={`axis-${i}`}
                                x1={centerX}
                                y1={centerY}
                                x2={point.x}
                                y2={point.y}
                                stroke="currentColor"
                                strokeWidth="1"
                                className="stroke-gray-300 dark:stroke-gray-600"
                            />
                        )
                    })}

                    {/* Data polygon */}
                    <polygon
                        points={dataPolygonPoints.map(p => `${p.x},${p.y}`).join(' ')}
                        fill="rgba(59, 130, 246, 0.3)"
                        stroke="rgb(59, 130, 246)"
                        strokeWidth="2"
                    />

                    {/* Data points */}
                    {dataPolygonPoints.map((point, i) => (
                        <circle
                            key={`point-${i}`}
                            cx={point.x}
                            cy={point.y}
                            r="4"
                            fill="rgb(59, 130, 246)"
                        />
                    ))}

                    {/* Labels */}
                    {dataPoints.map((point, i) => {
                        const angle = i * angleStep
                        const labelRadius = maxRadius + 30
                        const labelPos = polarToCartesian(centerX, centerY, labelRadius, angle)

                        // Adjust text anchor based on position
                        let textAnchor: 'start' | 'middle' | 'end' = 'middle'
                        if (labelPos.x > centerX + 5) textAnchor = 'start'
                        else if (labelPos.x < centerX - 5) textAnchor = 'end'

                        return (
                            <g key={`label-${i}`}>
                                <text
                                    x={labelPos.x}
                                    y={labelPos.y}
                                    textAnchor={textAnchor}
                                    fontSize="11"
                                    fontWeight="500"
                                    fill="currentColor"
                                    className="fill-gray-700 dark:fill-gray-300"
                                >
                                    {point.label}
                                </text>
                                <text
                                    x={labelPos.x}
                                    y={labelPos.y + 12}
                                    textAnchor={textAnchor}
                                    fontSize="10"
                                    fontWeight="bold"
                                    fill="currentColor"
                                    className="fill-blue-600 dark:fill-blue-400"
                                >
                                    {point.value}
                                </text>
                            </g>
                        )
                    })}
                </svg>
            </div>
        </div>
    )
}
