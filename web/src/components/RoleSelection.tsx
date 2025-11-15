import { roles } from '../constants/roles'

interface RoleSelectionProps {
  onSelect: (role: string) => void
}


export default function RoleSelection({ onSelect }: RoleSelectionProps) {
  const iconColorClasses = {
    gray: 'text-gray-600 dark:text-gray-400',
    red: 'text-red-600 dark:text-red-400',
    blue: 'text-blue-600 dark:text-blue-400',
    yellow: 'text-yellow-600 dark:text-yellow-400',
  }

  const borderColorClasses = {
    gray: 'hover:border-gray-500 dark:hover:border-gray-400',
    red: 'hover:border-red-500 dark:hover:border-red-400',
    blue: 'hover:border-blue-500 dark:hover:border-blue-400',
    yellow: 'hover:border-yellow-500 dark:hover:border-yellow-400',
  }

  return (
    <div className="animate-fade-in">
      <h2 className="block text-3xl font-medium text-gray-900 dark:text-white mb-10 text-center">
        What is your main responsibility in the organization?
      </h2>
      <div className="grid grid-cols-2 gap-6">
        {roles.map((role) => {
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
              <span className="text-xl font-medium text-gray-900 dark:text-white">{role.label}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
