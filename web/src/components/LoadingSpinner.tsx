interface LoadingSpinnerProps {
  message?: string
}

export default function LoadingSpinner({ message = 'Loading...' }: LoadingSpinnerProps) {
  return (
    <div className="animate-fade-in text-center">
      <div className="bg-white dark:bg-gray-700 rounded-2xl p-12 border border-gray-300 dark:border-gray-600">
        <div className="flex flex-col items-center gap-6">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 dark:border-blue-400"></div>
          <p className="text-xl text-gray-700 dark:text-gray-300">{message}</p>
        </div>
      </div>
    </div>
  )
}
