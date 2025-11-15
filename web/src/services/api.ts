import { type Assessment } from './types'

interface CreateAssessmentRequest {
  name: string
  role: string
  size: string
  risk: string
}

interface CreateAssessmentResponse {
  id: string
}

export async function createAssessment(data: CreateAssessmentRequest): Promise<string> {
  const response = await fetch('/api/assessments', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error('Failed to create assessment')
  }

  const result: CreateAssessmentResponse = await response.json()
  return result.id
}

export async function getAssessment(id: string): Promise<Assessment> {
  const response = await fetch(`/api/assessments/${id}`)

  if (!response.ok) {
    throw new Error('Failed to fetch assessment')
  }

  const assessment: Assessment = await response.json()
  return assessment
}

export type { Assessment, CreateAssessmentRequest }
