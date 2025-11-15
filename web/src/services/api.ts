interface CreateAssessmentRequest {
  name: string
  role: string
  size: string
  risk: string
}

interface CreateAssessmentResponse {
  id: string
}

interface Assessment {
  id: string
  metadata: {
    assessed_at: string
    role: string
    size: string
    risk: string
  }
  vendor: {
    name: string
    legal_name: string
    country: string
    url: string
  }
  application: {
    name: string
    description: string
    url: string
    category: string
    subcategory: string
  }
  trust_score: number
  confidence: number
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
