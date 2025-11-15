import { useState } from 'react'
import { ChevronDownIcon } from '@heroicons/react/24/outline'
import { roles } from '../constants/roles'

interface RoleDropdownProps {
  currentRole: string
  onRoleChange: (role: string) => void
}

export default function RoleDropdown({ currentRole, onRoleChange }: RoleDropdownProps) {
  const [isOpen, setIsOpen] = useState(false)

  const selectedRole = roles.find(r => r.id === currentRole)
  if (!selectedRole) return null

  const Icon = selectedRole.icon

  const colorClasses = {
    gray: 'bg-gray-600 hover:bg-gray-700 dark:bg-gray-500 dark:hover:bg-gray-600',
    red: 'bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600',
    blue: 'bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600',
    yellow: 'bg-yellow-600 hover:bg-yellow-700 dark:bg-yellow-500 dark:hover:bg-yellow-600',
    purple: 'bg-purple-600 hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600',
  }

  const iconColorClasses = {
    gray: 'text-gray-600 dark:text-gray-400',
    red: 'text-red-600 dark:text-red-400',
    blue: 'text-blue-600 dark:text-blue-400',
    yellow: 'text-yellow-600 dark:text-yellow-400',
    purple: 'text-purple-600 dark:text-purple-400',
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`flex items-center justify-between px-4 py-2 text-white rounded-lg transition-colors ${colorClasses[selectedRole.color as keyof typeof colorClasses]}`}
      >
        <div className="flex items-center gap-2">
          <Icon className="h-5 w-5" />
          <span className="font-medium">{selectedRole.name}</span>
        </div>
        <ChevronDownIcon className="h-4 w-4" />
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-700 rounded-lg shadow-lg border border-gray-300 dark:border-gray-600 z-20">
            {roles.map((role) => {
              const RoleIcon = role.icon
              const iconColor = iconColorClasses[role.color as keyof typeof iconColorClasses]
              return (
                <button
                  key={role.id}
                  onClick={() => {
                    onRoleChange(role.id)
                    setIsOpen(false)
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors first:rounded-t-lg last:rounded-b-lg ${
                    role.id === currentRole ? 'bg-gray-50 dark:bg-gray-600/50' : ''
                  }`}
                >
                  <RoleIcon className={`h-5 w-5 ${iconColor}`} />
                  <div className="flex flex-col items-start">
                    <span className="text-gray-900 dark:text-white">{role.name}</span>
                  </div>
                </button>
              )
            })}
          </div>
        </>
      )}
    </div>
  )
}
