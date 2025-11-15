import Header from './components/Header'
import AssessmentWorkflow from './components/AssessmentWorkflow'

function App() {
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-800">
      <Header />

      <main className="flex items-center justify-center h-[calc(100vh-5rem)] px-4 -mt-32">
        <AssessmentWorkflow />
      </main>
    </div>
  )
}

export default App
