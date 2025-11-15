import { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import Header from './components/Header'
import AssessmentWorkflow from './components/AssessmentWorkflow'

function App() {
  const navigate = useNavigate()
  const location = useLocation()
  const [currentRole, setCurrentRole] = useState<string>()

  // Sync currentRole with query params
  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const roleFromUrl = params.get('role')
    setCurrentRole(roleFromUrl || undefined)
  }, [location.search])

  const handleReset = () => {
    // Clear role locally
    setCurrentRole(undefined)
    // Navigate to root
    navigate('/')
  }

  const handleRoleChange = (role: string) => {
    setCurrentRole(role)
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-800">
      <Header onClearRole={handleReset} currentRole={currentRole} onRoleChange={handleRoleChange} />

      <main className="flex items-center justify-center h-[calc(100vh-5rem)] px-4 -mt-32">
        <Routes>
          <Route path="/*" element={<AssessmentWorkflow onRoleChange={handleRoleChange} />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
