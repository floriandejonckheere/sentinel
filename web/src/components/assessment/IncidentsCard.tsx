import React from 'react'

interface IncidentsCardProps {
  incidents: {
    total: number
    critical: number
    high: number
    medium: number
    low: number
    trend: 'improving' | 'stable' | 'declining'
  }
}

interface PieSlice {
  value: number
  color: string
  label: string
  startAngle: number
  endAngle: number
}

function getTrendIcon(trend: string): string {
  if (trend === 'improving') return '↓'
  if (trend === 'declining') return '↑'
  return '→'
}

function getTrendColor(trend: string): string {
  if (trend === 'improving') return 'text-green-600 dark:text-green-400'
  if (trend === 'declining') return 'text-red-600 dark:text-red-400'
  return 'text-blue-600 dark:text-blue-400'
}

function getTrendText(trend: string): string {
  if (trend === 'improving') return 'Improving'
  if (trend === 'declining') return 'Declining'
  return 'Stable'
}

function createPieSlices(incidents: IncidentsCardProps['incidents']): PieSlice[] {
  const data = [
    { value: incidents.critical, color: '#dc2626', label: 'Critical' },
    { value: incidents.high, color: '#ea580c', label: 'High' },
    { value: incidents.medium, color: '#ca8a04', label: 'Medium' },
    { value: incidents.low, color: '#16a34a', label: 'Low' },
  ]

  const total = incidents.total || 1
  let currentAngle = 0

  return data.map((item) => {
    const percentage = item.value / total
    const angle = percentage * 360
    const slice: PieSlice = {
      ...item,
      startAngle: currentAngle,
      endAngle: currentAngle + angle,
    }
    currentAngle += angle
    return slice
  })
}

function polarToCartesian(centerX: number, centerY: number, radius: number, angleInDegrees: number) {
  const angleInRadians = ((angleInDegrees - 90) * Math.PI) / 180.0
  return {
    x: centerX + radius * Math.cos(angleInRadians),
    y: centerY + radius * Math.sin(angleInRadians),
  }
}

function describeArc(centerX: number, centerY: number, radius: number, startAngle: number, endAngle: number): string {
  const start = polarToCartesian(centerX, centerY, radius, startAngle)
  const end = polarToCartesian(centerX, centerY, radius, endAngle)

  const arcSweep = endAngle - startAngle
  const largeArcFlag = arcSweep > 180 ? 1 : 0

  if (arcSweep >= 360) {
    // Full circle
    const mid = polarToCartesian(centerX, centerY, radius, startAngle + 180)
    return [
      'M', start.x, start.y,
      'A', radius, radius, 0, 1, 1, mid.x, mid.y,
      'A', radius, radius, 0, 1, 1, start.x, start.y,
      'Z'
    ].join(' ')
  }

  return [
    'M', centerX, centerY,
    'L', start.x, start.y,
    'A', radius, radius, 0, largeArcFlag, 1, end.x, end.y,
    'Z'
  ].join(' ')
}

function getLabelPosition(centerX: number, centerY: number, outerRadius: number, innerRadius: number, startAngle: number, endAngle: number) {
  const midAngle = (startAngle + endAngle) / 2
  const labelRadius = (outerRadius + innerRadius) / 2
  return polarToCartesian(centerX, centerY, labelRadius, midAngle)
}

export default function IncidentsCard({ incidents }: IncidentsCardProps) {
  const [hoveredSlice, setHoveredSlice] = React.useState<string | null>(null)
  const [tooltipPos, setTooltipPos] = React.useState({ x: 0, y: 0 })

  const slices = createPieSlices(incidents)
  const centerX = 150
  const centerY = 150
  const outerRadius = 100
  const innerRadius = 60

  const handleMouseMove = (e: React.MouseEvent<SVGPathElement>, label: string) => {
    const rect = e.currentTarget.ownerSVGElement?.getBoundingClientRect()
    if (rect) {
      setTooltipPos({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      })
    }
    setHoveredSlice(label)
  }

  const handleMouseLeave = () => {
    setHoveredSlice(null)
  }

  return (
    <div className="bg-white dark:bg-gray-700 rounded-2xl p-6 border border-gray-300 dark:border-gray-600 shadow-lg">
      <h4 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-4 text-center">
        Incidents
      </h4>

      {/* First Row: Pie Chart */}
      <div className="flex justify-center mb-3">
        {/* Donut Chart with Total in Center */}
        <div className="relative">
          <svg width="250" height="250" viewBox="0 0 300 300">
            {/* Donut Chart Rings */}
            {incidents.total > 0 ? (
              <>
                {slices.map((slice, index) => {
                  if (slice.value === 0) return null
                  return (
                    <path
                      key={index}
                      d={describeArc(centerX, centerY, outerRadius, slice.startAngle, slice.endAngle)}
                      fill={slice.color}
                      opacity={hoveredSlice === slice.label ? "1" : "0.9"}
                      style={{ cursor: 'pointer', transition: 'opacity 0.2s' }}
                      onMouseMove={(e) => handleMouseMove(e, slice.label)}
                      onMouseLeave={handleMouseLeave}
                    />
                  )
                })}
                {/* Inner circle cutout to create donut */}
                <circle cx={centerX} cy={centerY} r={innerRadius} fill="currentColor" className="fill-white dark:fill-gray-700" />

                {/* Individual counts on slices */}
                {slices.map((slice, index) => {
                  if (slice.value === 0) return null
                  const labelPos = getLabelPosition(centerX, centerY, outerRadius, innerRadius, slice.startAngle, slice.endAngle)
                  return (
                    <text
                      key={`label-${index}`}
                      x={labelPos.x}
                      y={labelPos.y}
                      textAnchor="middle"
                      fontSize="16"
                      fontWeight="bold"
                      fill="white"
                      style={{ pointerEvents: 'none' }}
                    >
                      {slice.value}
                    </text>
                  )
                })}
              </>
            ) : (
              <>
                <circle cx={centerX} cy={centerY} r={outerRadius} fill="#e5e7eb" />
                <circle cx={centerX} cy={centerY} r={innerRadius} fill="currentColor" className="fill-white dark:fill-gray-700" />
              </>
            )}

            {/* Total Incidents in Center */}
            <g transform={`translate(${centerX}, ${centerY})`}>
              <text
                x="0"
                y="8"
                textAnchor="middle"
                fontSize="36"
                fontWeight="bold"
                fill="currentColor"
                className="fill-gray-900 dark:fill-white"
              >
                {incidents.total}
              </text>
              <text
                x="0"
                y="24"
                textAnchor="middle"
                fontSize="10"
                fill="currentColor"
                className="fill-gray-500 dark:fill-gray-400"
              >
                Total Incidents
              </text>
            </g>

            {/* Tooltip */}
            {hoveredSlice && (
              <g transform={`translate(${tooltipPos.x}, ${tooltipPos.y - 10})`}>
                <rect
                  x="-30"
                  y="-20"
                  width="60"
                  height="20"
                  rx="4"
                  fill="currentColor"
                  className="fill-gray-900 dark:fill-gray-100"
                  opacity="0.9"
                />
                <text
                  x="0"
                  y="-6"
                  textAnchor="middle"
                  fontSize="11"
                  fontWeight="600"
                  fill="currentColor"
                  className="fill-white dark:fill-gray-900"
                >
                  {hoveredSlice}
                </text>
              </g>
            )}
          </svg>
        </div>
      </div>

      {/* Second Row: Trend and Explanation */}
      <div className="grid grid-cols-2 gap-3">
        {/* Left Column: Trend */}
        <div className="flex flex-col items-center justify-center gap-1">
          <span className={`text-4xl font-bold ${getTrendColor(incidents.trend)}`}>
            {getTrendIcon(incidents.trend)}
          </span>
          <span className={`text-base font-medium ${getTrendColor(incidents.trend)}`}>
            {getTrendText(incidents.trend)}
          </span>
        </div>

        {/* Right Column: Explanation */}
        <div className="flex items-center">
          <p className="text-xs text-gray-500 dark:text-gray-400 text-justify">
            Reported security breaches and events involving the application, categorized by severity levels. Trend indicates whether the incident frequency is improving, stable, or declining over time.
          </p>
        </div>
      </div>
    </div>
  )
}
