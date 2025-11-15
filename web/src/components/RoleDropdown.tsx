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

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors w-44"
      >
        <Icon className="h-5 w-5" />
        <span className="font-medium">{selectedRole.label}</span>
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
              return (
                <button
                  key={role.id}
                  onClick={() => {
                    onRoleChange(role.id)
                    setIsOpen(false)
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors first:rounded-t-lg last:rounded-b-lg ${
                    role.id === currentRole ? 'bg-blue-50 dark:bg-blue-900/20' : ''
                  }`}
                >
                  <RoleIcon className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                  <span className="text-gray-900 dark:text-white">{role.label}</span>
                </button>
              )
            })}
          </div>
        </>
      )}
    </div>
  )
}
