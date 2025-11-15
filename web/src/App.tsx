import { useState } from 'react'
import Header from './components/Header'
import AssessmentWorkflow from './components/AssessmentWorkflow'

function App() {
  const [workflowKey, setWorkflowKey] = useState(0)

  const handleReset = () => {
    setWorkflowKey(prev => prev + 1)
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-800">
      <Header onReset={handleReset} />

      <main className="flex items-center justify-center h-[calc(100vh-5rem)] px-4 -mt-32">
        <AssessmentWorkflow key={workflowKey} />
      </main>
    </div>
  )
}

export default App
