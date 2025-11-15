export interface Assessment {
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
  confidence: string
}
