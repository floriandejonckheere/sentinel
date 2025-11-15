import { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import Home from './components/Home'
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

  // Handler for dropdown role changes - updates URL
  const handleDropdownRoleChange = (role: string) => {
    setCurrentRole(role)
    // Update URL query params to sync with workflow
    const params = new URLSearchParams(location.search)
    params.set('role', role)
    navigate(`${location.pathname}?${params.toString()}`)
  }

  // Handler for workflow role changes - just updates state
  const handleWorkflowRoleChange = (role: string) => {
    setCurrentRole(role)
  }

  const isHomePage = location.pathname === '/'

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-800">
      <Header onClearRole={handleReset} currentRole={currentRole} onRoleChange={handleDropdownRoleChange} />

      <main className={`flex items-center justify-center px-4 ${isHomePage ? 'h-[calc(100vh-5rem)] -mt-32' : 'h-[calc(100vh-5rem)] -mt-32'}`}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/name" element={<AssessmentWorkflow onRoleChange={handleWorkflowRoleChange} />} />
          <Route path="/role" element={<AssessmentWorkflow onRoleChange={handleWorkflowRoleChange} />} />
          <Route path="/size" element={<AssessmentWorkflow onRoleChange={handleWorkflowRoleChange} />} />
          <Route path="/risk" element={<AssessmentWorkflow onRoleChange={handleWorkflowRoleChange} />} />
          <Route path="/complete" element={<AssessmentWorkflow onRoleChange={handleWorkflowRoleChange} />} />
        </Routes>
      </main>

      <Footer />
    </div>
  )
}

export default App
