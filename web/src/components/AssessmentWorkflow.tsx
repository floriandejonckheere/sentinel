import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import ApplicationInput from './ApplicationInput'
import RoleSelection from './RoleSelection'
import OrganizationSize from './OrganizationSize'
import RiskTolerance from './RiskTolerance'

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

export default function AssessmentWorkflow({ onRoleChange }: AssessmentWorkflowProps) {
  const navigate = useNavigate()
  const location = useLocation()

  // Determine initial step from URL
  const getStepFromPath = (path: string): Step => {
    if (path === '/' || path === '/application') return 'application'
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
    const path = step === 'application' ? '/' : `/${step}`
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

  const handleRiskSelect = (tolerance: number) => {
    const newData = { ...assessmentData, riskTolerance: tolerance }
    setAssessmentData(newData)
    navigateToStep('complete', newData)
  }

  return (
    <div className="w-full max-w-3xl">
      {currentStep === 'application' && (
        <ApplicationInput onSubmit={handleApplicationSubmit} />
      )}

      {currentStep === 'role' && (
        <RoleSelection onSelect={handleRoleSelect} />
      )}

      {currentStep === 'size' && (
        <OrganizationSize onSelect={handleSizeSelect} />
      )}

      {currentStep === 'risk' && (
        <RiskTolerance onSelect={handleRiskSelect} />
      )}

      {currentStep === 'complete' && (
        <div className="animate-fade-in text-center">
          <h2 className="text-3xl font-medium text-gray-900 dark:text-white mb-6">
            Assessment Complete
          </h2>
          <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600">
            <p className="text-lg text-gray-700 dark:text-gray-300 mb-4">
              <span className="font-semibold">Application:</span> {assessmentData.application}
            </p>
            <p className="text-lg text-gray-700 dark:text-gray-300 mb-4">
              <span className="font-semibold">Role:</span> {assessmentData.role}
            </p>
            <p className="text-lg text-gray-700 dark:text-gray-300 mb-4">
              <span className="font-semibold">Organization Size:</span> {assessmentData.organizationSize}
            </p>
            <p className="text-lg text-gray-700 dark:text-gray-300">
              <span className="font-semibold">Risk Tolerance:</span> {RISK_LABELS[assessmentData.riskTolerance]}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
