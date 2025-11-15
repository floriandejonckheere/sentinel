import { UsersIcon } from '@heroicons/react/24/outline'
import { ChevronLeftIcon } from '@heroicons/react/24/outline'

interface OrganizationSizeProps {
  onSelect: (size: string) => void
  onBack?: () => void
}

const sizes = [
  { id: '1-10', label: '1-10' },
  { id: '10-100', label: '10-100' },
  { id: '100+', label: '100+' },
]

export default function OrganizationSize({ onSelect, onBack }: OrganizationSizeProps) {
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
        <h2 className="text-3xl font-medium text-gray-900 dark:text-white text-center">
          What is the size of your organization?
        </h2>
      </div>
      <div className="flex flex-row gap-6 justify-center">
        {sizes.map((size) => (
          <button
            key={size.id}
            onClick={() => onSelect(size.id)}
            className="flex flex-col items-center justify-center gap-4 p-8 bg-white dark:bg-gray-700 rounded-2xl border border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 hover:shadow-lg transition-all min-w-[160px]"
          >
            <UsersIcon className="h-10 w-10 text-blue-600 dark:text-blue-400" />
            <span className="text-2xl font-medium text-gray-900 dark:text-white">{size.label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
