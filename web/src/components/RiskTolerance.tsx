import { useState } from 'react'
import { ChartBarIcon } from '@heroicons/react/24/outline'

interface RiskToleranceProps {
  onSelect: (tolerance: number) => void
}

const toleranceLabels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']

export default function RiskTolerance({ onSelect }: RiskToleranceProps) {
  const [value, setValue] = useState(2) // Default to Medium (index 2)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(parseInt(e.target.value))
  }

  const handleSubmit = () => {
    onSelect(value)
  }

  return (
    <div className="animate-fade-in">
      <h2 className="block text-3xl font-medium text-gray-900 dark:text-white mb-10 text-center">
        What is your risk tolerance?
      </h2>
      <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600 max-w-2xl mx-auto">
        <div className="flex justify-center mb-6">
          <ChartBarIcon className="h-12 w-12 text-blue-600 dark:text-blue-400" />
        </div>

        <div className="mb-8">
          <div className="text-center mb-6">
            <span className="text-3xl font-semibold text-blue-600 dark:text-blue-400">
              {toleranceLabels[value]}
            </span>
          </div>

          <input
            type="range"
            min="0"
            max="4"
            step="1"
            value={value}
            onChange={handleChange}
            className="w-full h-3 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
            style={{
              background: `linear-gradient(to right, rgb(59, 130, 246) 0%, rgb(59, 130, 246) ${(value / 4) * 100}%, rgb(229, 231, 235) ${(value / 4) * 100}%, rgb(229, 231, 235) 100%)`
            }}
          />

          <div className="flex justify-between mt-2 text-sm text-gray-600 dark:text-gray-400">
            {toleranceLabels.map((label, index) => (
              <span key={index} className={value === index ? 'font-semibold text-blue-600 dark:text-blue-400' : ''}>
                {label}
              </span>
            ))}
          </div>
        </div>

        <div className="flex justify-center">
          <button
            onClick={handleSubmit}
            className="px-8 py-3 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white font-medium rounded-lg transition-colors"
          >
            Continue
          </button>
        </div>
      </div>
    </div>
  )
}
