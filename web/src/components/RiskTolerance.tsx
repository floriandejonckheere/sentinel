import { useState } from 'react'
import { ChartBarIcon, ChevronLeftIcon } from '@heroicons/react/24/outline'
import { riskLevels } from '../constants/risk'

interface RiskToleranceProps {
  onSelect: (tolerance: number) => void
  onBack?: () => void
}

export default function RiskTolerance({ onSelect, onBack }: RiskToleranceProps) {
  const [value, setValue] = useState(1) // Default to Medium (index 1)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(parseInt(e.target.value))
  }

  const handleSubmit = () => {
    onSelect(value)
  }

  return (
    <div className="animate-fade-in">
      <div className="flex items-center justify-center mb-10 gap-4">
        {onBack && (
          <ChevronLeftIcon
            role="button"
            tabIndex={0}
            aria-label="Back"
            onClick={onBack}
            onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') onBack() }}
            className="h-10 w-10 p-1 rounded-xl text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-gray-100 dark:hover:bg-gray-600 transition cursor-pointer"
          />
        )}
        <h2 className="block text-3xl font-medium text-gray-900 dark:text-white text-center">
          What is your risk tolerance?
        </h2>
      </div>
      <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600 max-w-2xl mx-auto">
        <div className="flex justify-center mb-6">
          <ChartBarIcon className={`h-12 w-12 ${riskLevels[value].color.text}`} />
        </div>

        <div className="mb-8">
          <div className="text-center mb-6">
            <span className={`text-3xl font-semibold ${riskLevels[value].color.text}`}>
              {riskLevels[value].name}
            </span>
          </div>

          <style>{`
            .risk-slider-${value}::-webkit-slider-thumb {
              appearance: none;
              width: 20px;
              height: 20px;
              border-radius: 50%;
              background: ${riskLevels[value].color.bg};
              cursor: pointer;
              border: 2px solid white;
              box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            .risk-slider-${value}::-moz-range-thumb {
              width: 20px;
              height: 20px;
              border-radius: 50%;
              background: ${riskLevels[value].color.bg};
              cursor: pointer;
              border: 2px solid white;
              box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
          `}</style>

          <input
            type="range"
            min="0"
            max="2"
            step="1"
            value={value}
            onChange={handleChange}
            className={`w-full h-3 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer risk-slider-${value}`}
            style={{
              background: `linear-gradient(to right, ${riskLevels[value].color.bg} 0%, ${riskLevels[value].color.bg} ${(value / 2) * 100}%, rgb(229, 231, 235) ${(value / 2) * 100}%, rgb(229, 231, 235) 100%)`
            }}
          />

          <div className="flex justify-between mt-2 text-sm text-gray-600 dark:text-gray-400">
            {riskLevels.map((level, index) => (
              <span key={index} className={value === index ? `font-semibold ${riskLevels[index].color.text}` : ''}>
                {level.name}
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
