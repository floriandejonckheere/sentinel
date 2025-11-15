import { UsersIcon } from '@heroicons/react/24/outline'

interface OrganizationSizeProps {
  onSelect: (size: string) => void
}

const sizes = [
  { id: '1-10', label: '1-10' },
  { id: '10-100', label: '10-100' },
  { id: '100+', label: '100+' },
]

export default function OrganizationSize({ onSelect }: OrganizationSizeProps) {
  return (
    <div className="animate-fade-in">
      <h2 className="block text-3xl font-medium text-gray-900 dark:text-white mb-10 text-center">
        What is the size of your organization?
      </h2>
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
