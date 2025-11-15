import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import ApplicationInput from './ApplicationInput'
import RoleSelection from './RoleSelection'
import OrganizationSize from './OrganizationSize'
import RiskTolerance from './RiskTolerance'
import LoadingSpinner from './LoadingSpinner'
import { riskLevels } from '../constants/risk'
import { createAssessment } from '../services/api'

type Step = 'application' | 'role' | 'size' | 'risk' | 'complete'

interface AssessmentData {
  application: string
  role: string
  organizationSize: string
  riskTolerance: number
}

interface AssessmentWorkflowProps {
  onRoleChange?: (role: string) => void
}

const RISK_LABELS = ['Low', 'Medium', 'High']

const LOADING_MESSAGES = [
  "Creating your security assessment...",
  "Analyzing vulnerability databases...",
  "Reviewing compliance frameworks...",
  "Scanning CVE repositories...",
  "Evaluating security posture...",
  "Generating trust brief...",
]

export default function AssessmentWorkflow({ onRoleChange }: AssessmentWorkflowProps) {
  const navigate = useNavigate()
  const location = useLocation()

  // Determine initial step from URL
  const getStepFromPath = (path: string): Step => {
    if (path === '/name') return 'application'
    if (path === '/role') return 'role'
    if (path === '/size') return 'size'
    if (path === '/risk') return 'risk'
    if (path === '/complete') return 'complete'
    return 'application'
  }

  // Load data from query parameters
  const loadDataFromQuery = (): AssessmentData => {
    const params = new URLSearchParams(location.search)
    const riskLabel = params.get('risk') || ''
    const riskIndex = RISK_LABELS.indexOf(riskLabel)

    return {
      application: params.get('name') || '',
      role: params.get('role') || '',
      organizationSize: params.get('size') || '',
      riskTolerance: riskIndex >= 0 ? riskIndex : 1,
    }
  }

  const [currentStep, setCurrentStep] = useState<Step>(() => getStepFromPath(location.pathname))
  const [assessmentData, setAssessmentData] = useState<AssessmentData>(loadDataFromQuery)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0)

  // Sync step and data with URL changes
  useEffect(() => {
    const step = getStepFromPath(location.pathname)
    setCurrentStep(step)
    setAssessmentData(loadDataFromQuery())
  }, [location.pathname, location.search])

  // Restore role in header when component mounts or data changes
  useEffect(() => {
    if (assessmentData.role && onRoleChange) {
      onRoleChange(assessmentData.role)
    }
  }, [assessmentData.role, onRoleChange])

  // Rotate loading messages every 10 seconds
  useEffect(() => {
    if (!isLoading) {
      setLoadingMessageIndex(0)
      return
    }

    const interval = setInterval(() => {
      setLoadingMessageIndex((prevIndex) => (prevIndex + 1) % LOADING_MESSAGES.length)
    }, 5000) // 5 seconds

    return () => clearInterval(interval)
  }, [isLoading])

  const buildQueryString = (data: Partial<AssessmentData>): string => {
    const params = new URLSearchParams()
    if (data.application) params.set('name', data.application)
    if (data.role) params.set('role', data.role)
    if (data.organizationSize) params.set('size', data.organizationSize)
    if (data.riskTolerance !== undefined) params.set('risk', RISK_LABELS[data.riskTolerance])

    const queryString = params.toString()
    return queryString ? `?${queryString}` : ''
  }

  const navigateToStep = (step: Step, data: AssessmentData) => {
    const path = step === 'application' ? '/name' : `/${step}`
    const query = buildQueryString(data)
    navigate(`${path}${query}`)
  }

  const handleApplicationSubmit = (value: string) => {
    const newData = { ...assessmentData, application: value }
    setAssessmentData(newData)
    navigateToStep('role', newData)
  }

  const handleRoleSelect = (role: string) => {
    const newData = { ...assessmentData, role }
    setAssessmentData(newData)
    onRoleChange?.(role)
    navigateToStep('size', newData)
  }

  const handleSizeSelect = (size: string) => {
    const newData = { ...assessmentData, organizationSize: size }
    setAssessmentData(newData)
    navigateToStep('risk', newData)
  }

  const handleRiskSelect = async (tolerance: number) => {
    const newData = { ...assessmentData, riskTolerance: tolerance }
    setAssessmentData(newData)
    navigateToStep('complete', newData)
  }

  // Create assessment when arriving at complete step
  useEffect(() => {
    if (currentStep === 'complete' && !isLoading && !error) {
      handleCreateAssessment()
    }
  }, [currentStep])

  const handleCreateAssessment = async () => {
    setIsLoading(true)
    setError(null)

    try {
      // Map risk tolerance index to key
      const riskKey = riskLevels[assessmentData.riskTolerance]?.id || 'medium'

      // POST to create assessment
      const assessmentId = await createAssessment({
        name: assessmentData.application,
        role: assessmentData.role,
        size: assessmentData.organizationSize,
        risk: riskKey,
      })

      // Redirect to the assessment details page with role query param
      const roleParam = assessmentData.role ? `?role=${encodeURIComponent(assessmentData.role)}` : ''
      navigate(`/assessments/${assessmentId}${roleParam}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setIsLoading(false)
    }
  }

  const handleBackFromRole = () => {
    // Back to application
    navigateToStep('application', assessmentData)
  }

  const handleBackFromSize = () => {
    navigateToStep('role', assessmentData)
  }

  const handleBackFromRisk = () => {
    navigateToStep('size', assessmentData)
  }

  return (
    <div className="w-full max-w-3xl">
      {currentStep === 'application' && (
        <ApplicationInput onSubmit={handleApplicationSubmit} />
      )}

      {currentStep === 'role' && (
        <RoleSelection onSelect={handleRoleSelect} onBack={handleBackFromRole} />
      )}

      {currentStep === 'size' && (
        <OrganizationSize onSelect={handleSizeSelect} onBack={handleBackFromSize} />
      )}

      {currentStep === 'risk' && (
        <RiskTolerance onSelect={handleRiskSelect} onBack={handleBackFromRisk} />
      )}

      {currentStep === 'complete' && (
        <>
          {isLoading && <LoadingSpinner message={LOADING_MESSAGES[loadingMessageIndex]} />}

          {error && (
            <div className="animate-fade-in text-center">
              <div className="bg-red-50 dark:bg-red-900/20 rounded-2xl p-8 border border-red-300 dark:border-red-600">
                <h2 className="text-2xl font-medium text-red-900 dark:text-red-200 mb-4">
                  Error
                </h2>
                <p className="text-red-700 dark:text-red-300">{error}</p>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
