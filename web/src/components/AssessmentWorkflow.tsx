import { useState } from 'react'
import ApplicationInput from './ApplicationInput'
import RoleSelection from './RoleSelection'
import OrganizationSize from './OrganizationSize'

type Step = 'application' | 'role' | 'size' | 'complete'

interface AssessmentData {
  application: string
  role: string
  organizationSize: string
}

export default function AssessmentWorkflow() {
  const [currentStep, setCurrentStep] = useState<Step>('application')
  const [assessmentData, setAssessmentData] = useState<AssessmentData>({
    application: '',
    role: '',
    organizationSize: '',
  })

  const handleApplicationSubmit = (value: string) => {
    setAssessmentData(prev => ({ ...prev, application: value }))
    setCurrentStep('role')
  }

  const handleRoleSelect = (role: string) => {
    setAssessmentData(prev => ({ ...prev, role }))
    setCurrentStep('size')
  }

  const handleSizeSelect = (size: string) => {
    setAssessmentData(prev => ({ ...prev, organizationSize: size }))
    setCurrentStep('complete')
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
            <p className="text-lg text-gray-700 dark:text-gray-300">
              <span className="font-semibold">Organization Size:</span> {assessmentData.organizationSize}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
