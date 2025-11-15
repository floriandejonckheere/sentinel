import { ShieldCheckIcon, CogIcon, BriefcaseIcon, ClipboardDocumentCheckIcon } from '@heroicons/react/24/outline'

interface RoleSelectionProps {
  onSelect: (role: string) => void
}

const roles = [
  { id: 'executive', label: 'Executive', icon: BriefcaseIcon },
  { id: 'security', label: 'Security', icon: ShieldCheckIcon },
  { id: 'compliance', label: 'Compliance', icon: ClipboardDocumentCheckIcon },
  { id: 'technical', label: 'Technical', icon: CogIcon },
]

export default function RoleSelection({ onSelect }: RoleSelectionProps) {
  return (
    <div className="animate-fade-in">
      <h2 className="block text-3xl font-medium text-gray-900 dark:text-white mb-10 text-center">
        What is your main responsibility in the organization?
      </h2>
      <div className="grid grid-cols-2 gap-6">
        {roles.map((role) => {
          const Icon = role.icon
          return (
            <button
              key={role.id}
              onClick={() => onSelect(role.id)}
              className="flex flex-col items-center justify-center p-8 bg-white dark:bg-gray-700 rounded-2xl border border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 hover:shadow-lg transition-all"
            >
              <Icon className="h-16 w-16 text-blue-600 dark:text-blue-400 mb-4" />
              <span className="text-xl font-medium text-gray-900 dark:text-white">{role.label}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
