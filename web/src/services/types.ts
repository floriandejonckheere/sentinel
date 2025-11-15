export interface Assessment {
    id: string
    metadata: {
        assessed_at: string
    }
    vendor: {
        name: string
        legal_name: string
        country: string
        url: string
    }
    application: {
        application_intel: {
            name: string
            vendorName: string
        }
        description: string
        url: string
        category: string
        subcategory: string
    }
    summary: {
        trust_score: {
            score: number
            confidence: "low" | "medium" | "high"
            trend: "improving" | "stable" | "declining"

            architecture: number
            data_protection: number
            identity_access: number
            devsecops: number
            historical_security: number
            compliance: number
            platform_security: number
            risks_exposure: number
        }
        key_strengths: string[]
        key_risks: string[]
    }
    architecture: {
        encryption: string
        key_derivation: string
        zero_knowledge: boolean
        open_source: boolean
        authentication: string
        deployment: "on-premise" | "cloud" | "saas" | "hybrid"
    }
    compliance: {
        certs: {
            name: string
            status: "active" | "expired" | "pending"
            issued_by: string
            issue_date: string
            expiry_date: string
            url: string
        }[]
        frameworks: {
            name: string
            compliance_level: "compliant" | "non-compliant" | "partial"
            last_audit_date: string
            url: string
        }[]
        data_residency: string[]
    }
    cves: {
        total: number
        critical: number
        high: number
        medium: number
        low: number
        unknown: number

        trend: "improving" | "stable" | "declining"
    }
    incidents: {
        total: number
        critical: number
        high: number
        medium: number
        low: number

        trend: "improving" | "stable" | "declining"
    }
    alternatives: {
        name: string
        url: string
        trust_score: number
    }
}
