import { roles } from '../constants/roles'
import { ChevronLeftIcon } from '@heroicons/react/24/outline'

interface RoleSelectionProps {
  onSelect: (role: string) => void
  onBack?: () => void
}


export default function RoleSelection({ onSelect, onBack }: RoleSelectionProps) {
  const iconColorClasses = {
    gray: 'text-gray-600 dark:text-gray-400',
    red: 'text-red-600 dark:text-red-400',
    blue: 'text-blue-600 dark:text-blue-400',
    yellow: 'text-yellow-600 dark:text-yellow-400',
    purple: 'text-purple-600 dark:text-purple-400',
  }

  const borderColorClasses = {
    gray: 'hover:border-gray-500 dark:hover:border-gray-400',
    red: 'hover:border-red-500 dark:hover:border-red-400',
    blue: 'hover:border-blue-500 dark:hover:border-blue-400',
    yellow: 'hover:border-yellow-500 dark:hover:border-yellow-400',
    purple: 'hover:border-purple-500 dark:hover:border-purple-400',
  }

  const mainRoles = roles.filter(role => role.id !== 'global')
  const allRole = roles.find(role => role.id === 'global')

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
          What is your main responsibility in the organization?
        </h2>
      </div>
      <div className="grid grid-cols-2 gap-6">
        {mainRoles.map((role) => {
          const Icon = role.icon
          const iconColor = iconColorClasses[role.color as keyof typeof iconColorClasses]
          const borderColor = borderColorClasses[role.color as keyof typeof borderColorClasses]
          return (
            <button
              key={role.id}
              onClick={() => onSelect(role.id)}
              className={`flex flex-col items-center justify-center p-8 bg-white dark:bg-gray-700 rounded-2xl border border-gray-300 dark:border-gray-600 ${borderColor} hover:shadow-lg transition-all`}
            >
              <Icon className={`h-16 w-16 ${iconColor} mb-4`} />
              <span className="text-xl font-medium text-gray-900 dark:text-white">{role.description}</span>
            </button>
          )
        })}
      </div>
      {allRole && (
        <button
          onClick={() => onSelect(allRole.id)}
          className={`mt-6 w-full flex flex-col items-center justify-center p-8 bg-white dark:bg-gray-700 rounded-2xl border border-gray-300 dark:border-gray-600 ${borderColorClasses[allRole.color as keyof typeof borderColorClasses]} hover:shadow-lg transition-all`}
        >
          <allRole.icon className={`h-16 w-16 ${iconColorClasses[allRole.color as keyof typeof iconColorClasses]} mb-4`} />
          <span className="text-xl font-medium text-gray-900 dark:text-white">{allRole.description}</span>
        </button>
      )}
    </div>
  )
}
