import { ShieldCheckIcon } from '@heroicons/react/24/outline'
import RoleDropdown from './RoleDropdown'

interface HeaderProps {
  onClearRole: () => void
  currentRole?: string
  onRoleChange?: (role: string) => void
  disabled?: boolean
}

export default function Header({ onClearRole, currentRole, onRoleChange, disabled = false }: HeaderProps) {
  return (
    <header className="px-4 sm:px-6 py-3 sm:py-4 flex items-center justify-between">
      <button
        onClick={onClearRole}
        className="flex items-center gap-2 sm:gap-3 hover:opacity-80 transition-opacity"
      >
        <ShieldCheckIcon className="h-6 w-6 sm:h-8 sm:w-8 text-blue-600 dark:text-blue-400" />
        <h1 className="text-xl sm:text-2xl font-light text-gray-900 dark:text-white">Sentinel</h1>
      </button>

      {currentRole && onRoleChange && (
        <RoleDropdown currentRole={currentRole} onRoleChange={onRoleChange} disabled={disabled} />
      )}
    </header>
  )
}
