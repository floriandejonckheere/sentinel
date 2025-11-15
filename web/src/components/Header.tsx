import { ShieldCheckIcon } from '@heroicons/react/24/outline'
import RoleDropdown from './RoleDropdown'

interface HeaderProps {
  onReset: () => void
  currentRole?: string
  onRoleChange?: (role: string) => void
}

export default function Header({ onReset, currentRole, onRoleChange }: HeaderProps) {
  return (
    <header className="px-6 py-4 flex items-center justify-between">
      <button
        onClick={onReset}
        className="flex items-center gap-3 hover:opacity-80 transition-opacity"
      >
        <ShieldCheckIcon className="h-8 w-8 text-blue-600 dark:text-blue-400" />
        <h1 className="text-2xl font-light text-gray-900 dark:text-white">Sentinel</h1>
      </button>

      {currentRole && onRoleChange && (
        <RoleDropdown currentRole={currentRole} onRoleChange={onRoleChange} />
      )}
    </header>
  )
}
