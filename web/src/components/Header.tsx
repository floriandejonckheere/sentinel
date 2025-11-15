import { ShieldCheckIcon } from '@heroicons/react/24/outline'

interface HeaderProps {
  onReset: () => void
}

export default function Header({ onReset }: HeaderProps) {
  return (
    <header className="px-6 py-4">
      <button
        onClick={onReset}
        className="flex items-center gap-3 hover:opacity-80 transition-opacity"
      >
        <ShieldCheckIcon className="h-8 w-8 text-blue-600 dark:text-blue-400" />
        <h1 className="text-2xl font-light text-gray-900 dark:text-white">Sentinel</h1>
      </button>
    </header>
  )
}
