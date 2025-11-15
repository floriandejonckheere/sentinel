import {useState, useEffect} from 'react'
import {useParams, useSearchParams} from 'react-router-dom'
import {getAssessment, type Assessment} from '../services/api'
import LoadingSpinner from './LoadingSpinner'
import ApplicationVendorCard from './assessment/ApplicationVendorCard'
import TrustScoreCard from './assessment/TrustScoreCard'
import VulnerabilitiesCard from './assessment/VulnerabilitiesCard'
import SpiderChartCard from './assessment/SpiderChartCard'
import KeyTakeawaysCard from './assessment/KeyTakeawaysCard'
import ArchitectureCard from './assessment/ArchitectureCard'
import CertificationsCard from './assessment/CertificationsCard'
import ComplianceCard from './assessment/ComplianceCard'

export default function AssessmentDetails() {
    const {id} = useParams<{ id: string }>()
    const [searchParams] = useSearchParams()
    const role = searchParams.get('role')
    const [isLoading, setIsLoading] = useState(true)
    const [assessment, setAssessment] = useState<Assessment | null>(null)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (id) {
            fetchAssessment(id)
        }
    }, [id, role])

    const fetchAssessment = async (assessmentId: string) => {
        setIsLoading(true)
        setError(null)

        try {
            const fetchedAssessment = await getAssessment(assessmentId)
            setAssessment(fetchedAssessment)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred')
        } finally {
            setIsLoading(false)
        }
    }

    if (isLoading) {
        return <LoadingSpinner message="Loading assessment..."/>
    }

    if (error) {
        return (
            <div className="animate-fade-in text-center w-full max-w-3xl">
                <div className="bg-red-50 dark:bg-red-900/20 rounded-2xl p-8 border border-red-300 dark:border-red-600">
                    <h2 className="text-2xl font-medium text-red-900 dark:text-red-200 mb-4">
                        Error
                    </h2>
                    <p className="text-red-700 dark:text-red-300">{error}</p>
                </div>
            </div>
        )
    }

    if (!assessment) {
        return (
            <div className="animate-fade-in text-center w-full max-w-3xl">
                <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 border border-gray-300 dark:border-gray-600">
                    <p className="text-gray-700 dark:text-gray-300">Assessment not found</p>
                </div>
            </div>
        )
    }

    return (
        <div className="animate-fade-in w-full max-w-5xl px-4">
            <h2 className="text-3xl font-medium text-gray-900 dark:text-white mb-6 text-center">
                Security Assessment Details
            </h2>

            {/* Application & Vendor Card - Full Width */}
            <div className="mb-6">
                <ApplicationVendorCard
                    application={assessment.application}
                    vendor={assessment.vendor}
                    assessedAt={assessment.metadata.assessed_at}
                />
            </div>

            {/* All other cards - Two Column Flexbox Layout */}
            <div className="flex flex-wrap gap-6">
                <div className="flex-1 min-w-[calc(50%-0.75rem)]">
                    <TrustScoreCard
                        score={assessment.summary.trust_score.score}
                        confidence={assessment.summary.trust_score.confidence}
                    />
                </div>
                <div className="flex-1 min-w-[calc(50%-0.75rem)]">
                    <SpiderChartCard data={assessment.summary.trust_score}/>
                </div>
                <div className="flex-1 min-w-[calc(50%-0.75rem)]">
                    <VulnerabilitiesCard cves={assessment.cves}/>
                </div>
                <div className="flex-1 min-w-[calc(50%-0.75rem)]">
                    <KeyTakeawaysCard
                        strengths={assessment.summary.key_strengths}
                        risks={assessment.summary.key_risks}
                    />
                </div>
                <div className="flex-1 min-w-[calc(50%-0.75rem)]">
                    <ArchitectureCard architecture={assessment.architecture}/>
                </div>
                <div className="flex-1 min-w-[calc(50%-0.75rem)]">
                    <CertificationsCard certifications={assessment.compliance.certifications}/>
                </div>
                <div className="flex-1 min-w-[calc(50%-0.75rem)]">
                    <ComplianceCard
                        frameworks={assessment.compliance.frameworks}
                        dataResidency={assessment.compliance.data_residency}
                    />
                </div>
            </div>
        </div>
    )
}
