import { ShieldCheckIcon, PaperAirplaneIcon } from '@heroicons/react/24/outline'

function App() {
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-800">
      <header className="px-6 py-4">
        <div className="flex items-center gap-3">
          <ShieldCheckIcon className="h-8 w-8 text-blue-600 dark:text-blue-400" />
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Sentinel</h1>
        </div>
      </header>

      <main className="flex items-center justify-center h-[calc(100vh-5rem)] px-4 -mt-32">
        <div className="w-full max-w-3xl">
          <label htmlFor="app-input" className="block text-3xl font-medium text-gray-900 dark:text-white mb-10 text-center">
            Which application do you want to evaluate today?
          </label>
          <div className="relative">
            <input
              type="text"
              id="app-input"
              placeholder="Type an application name or URL"
              className="w-full px-6 py-4 pr-14 text-lg rounded-2xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="submit"
              className="absolute right-2 top-1/2 -translate-y-1/2 p-3 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-gray-600 rounded-2xl transition-colors"
            >
              <PaperAirplaneIcon className="h-6 w-6" />
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
