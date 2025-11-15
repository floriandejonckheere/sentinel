import { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import Home from './components/Home'
import AssessmentWorkflow from './components/AssessmentWorkflow'
import AssessmentDetails from './components/AssessmentDetails'

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
  const isAssessmentDetailsPage = location.pathname.startsWith('/assessments/')

  return (
  <div className="min-h-screen bg-gray-100 dark:bg-gray-800">
    {!isHomePage && (
      <Header
        onClearRole={handleReset}
        currentRole={currentRole}
        onRoleChange={handleDropdownRoleChange}
      />
    )}

    <main
      className={[
        "px-4", // shared

        // Home: fully centered hero layout
        isHomePage && "flex items-center justify-center min-h-screen",

        // Assessment details page: scrollable content, top-aligned
        !isHomePage && isAssessmentDetailsPage &&
          "min-h-[calc(100vh-5rem)] pt-24 pb-24 flex justify-center",

        // Wizard steps (/name, /role, /size, /risk, /complete):
        // top-aligned, scrollable, with room above footer
        !isHomePage && !isAssessmentDetailsPage &&
          "min-h-[calc(100vh-5rem)] pt-12 pb-24 flex justify-center",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/name" element={<AssessmentWorkflow onRoleChange={handleWorkflowRoleChange} />} />
        <Route path="/role" element={<AssessmentWorkflow onRoleChange={handleWorkflowRoleChange} />} />
        <Route path="/size" element={<AssessmentWorkflow onRoleChange={handleWorkflowRoleChange} />} />
        <Route path="/risk" element={<AssessmentWorkflow onRoleChange={handleWorkflowRoleChange} />} />
        <Route path="/complete" element={<AssessmentWorkflow onRoleChange={handleWorkflowRoleChange} />} />
        <Route path="/assessments/:id" element={<AssessmentDetails />} />
      </Routes>
    </main>

    {!isHomePage && <Footer />}
  </div>
);
}

export default App
