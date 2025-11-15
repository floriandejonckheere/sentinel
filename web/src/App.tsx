import { useState } from 'react'
import { Routes, Route, useNavigate } from 'react-router-dom'
import Header from './components/Header'
import AssessmentWorkflow from './components/AssessmentWorkflow'

function App() {
  const navigate = useNavigate()
  const [currentRole, setCurrentRole] = useState<string>()

  const handleReset = () => {
    setCurrentRole(undefined)
    navigate('/')
  }

  const handleRoleChange = (role: string) => {
    setCurrentRole(role)
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-800">
      <Header onReset={handleReset} currentRole={currentRole} onRoleChange={handleRoleChange} />

      <main className="flex items-center justify-center h-[calc(100vh-5rem)] px-4 -mt-32">
        <Routes>
          <Route path="/*" element={<AssessmentWorkflow onRoleChange={handleRoleChange} />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
