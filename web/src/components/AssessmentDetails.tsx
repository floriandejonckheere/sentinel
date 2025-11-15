import {useState, useEffect} from 'react'
import {useParams} from 'react-router-dom'
import {getAssessment, type Assessment} from '../services/api'
import LoadingSpinner from './LoadingSpinner'
import ApplicationVendorCard from './assessment/ApplicationVendorCard'
import TrustScoreCard from './assessment/TrustScoreCard'
import VulnerabilitiesCard from './assessment/VulnerabilitiesCard'
import SpiderChartCard from './assessment/SpiderChartCard'

export default function AssessmentDetails() {
    const {id} = useParams<{ id: string }>()
    const [isLoading, setIsLoading] = useState(true)
    const [assessment, setAssessment] = useState<Assessment | null>(null)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (id) {
            fetchAssessment(id)
        }
    }, [id])

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

            {/* First Row - Application & Vendor Card */}
            <div className="mb-6">
                <ApplicationVendorCard
                    application={assessment.application}
                    vendor={assessment.vendor}
                />
            </div>

            {/* Second Row - Trust Score & Spider Chart Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <TrustScoreCard
                    score={assessment.summary.trust_score.score}
                    confidence={assessment.summary.trust_score.confidence}
                />
                <SpiderChartCard data={assessment.summary.trust_score}/>
            </div>

            {/* Third Row - Vulnerabilities Card */}
            <div>
                <VulnerabilitiesCard cves={assessment.cves}/>
            </div>
        </div>
    )
}
