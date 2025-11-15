import { useState } from 'react'
import { PaperAirplaneIcon, ChevronLeftIcon } from '@heroicons/react/24/outline'

interface ApplicationInputProps {
  onSubmit: (value: string) => void
  onBack?: () => void
}

export default function ApplicationInput({ onSubmit, onBack }: ApplicationInputProps) {
  const [inputValue, setInputValue] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputValue.trim()) {
      onSubmit(inputValue)
    }
  }

  const handleExampleClick = (example: string) => {
    setInputValue(example)
    onSubmit(example)
  }

  const examples = ['1Password', 'Skype', 'CCleaner', 'Dropbox']

  return (
    <form onSubmit={handleSubmit} className="transition-opacity duration-500">
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
        <label htmlFor="app-input" className="text-3xl font-medium text-gray-900 dark:text-white text-center">
          Which application do you want to assess today?
        </label>
      </div>
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

      {/* Example buttons */}
      <div className="mt-6 flex flex-wrap justify-center gap-3">
        <span className="text-sm text-gray-500 dark:text-gray-400 self-center mr-2">
          Try an example:
        </span>
        {examples.map((example) => (
          <button
            key={example}
            type="button"
            onClick={() => handleExampleClick(example)}
            className="px-4 py-2 text-sm font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors"
          >
            {example}
          </button>
        ))}
      </div>
    </form>
  )
}
