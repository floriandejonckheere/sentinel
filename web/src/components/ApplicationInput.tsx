import { useState } from 'react'
import { PaperAirplaneIcon } from '@heroicons/react/24/outline'

interface ApplicationInputProps {
  onSubmit: (value: string) => void
}

export default function ApplicationInput({ onSubmit }: ApplicationInputProps) {
  const [inputValue, setInputValue] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputValue.trim()) {
      onSubmit(inputValue)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="transition-opacity duration-500">
      <label htmlFor="app-input" className="block text-3xl font-medium text-gray-900 dark:text-white mb-10 text-center">
        Which application do you want to assess today?
      </label>
      <div className="relative">
        <input
          type="text"
          id="app-input"
          value={inputValue}
          autoComplete="off"
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type an application name or URL"
          className="w-full px-6 py-4 pr-14 text-lg rounded-2xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          type="submit"
          disabled={!inputValue.trim()}
          className={`absolute right-2 top-1/2 -translate-y-1/2 p-3 rounded-2xl transition-colors ${
            inputValue.trim()
              ? 'text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-gray-600'
              : 'text-gray-400 dark:text-gray-600 cursor-not-allowed'
          }`}
        >
          <PaperAirplaneIcon className="h-6 w-6" />
        </button>
      </div>
    </form>
  )
}
