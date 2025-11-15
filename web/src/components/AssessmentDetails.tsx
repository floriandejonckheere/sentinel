import {useState, useEffect} from 'react'
import {useParams, useSearchParams} from 'react-router-dom'
import {getAssessment, type Assessment} from '../services/api'
import LoadingSpinner from './LoadingSpinner'
import ApplicationVendorCard from './assessment/ApplicationVendorCard'
import TrustScoreCard from './assessment/TrustScoreCard'
import VulnerabilitiesCard from './assessment/VulnerabilitiesCard'
import IncidentsCard from './assessment/IncidentsCard'
import SpiderChartCard from './assessment/SpiderChartCard'
import KeyTakeawaysCard from './assessment/KeyTakeawaysCard'
import ArchitectureCard from './assessment/ArchitectureCard'
import CertificationsCard from './assessment/CertificationsCard'
import ComplianceCard from './assessment/ComplianceCard'
import AlternativesCard from './assessment/AlternativesCard'
import RecentCVEsCard from './assessment/RecentCVEsCard'
import RecentIncidentsCard from './assessment/RecentIncidentsCard'

export default function AssessmentDetails() {
    const {id} = useParams<{ id: string }>()
    const [searchParams] = useSearchParams()
    const role = searchParams.get('role')
    const [isLoading, setIsLoading] = useState(true)
    const [assessment, setAssessment] = useState<Assessment | null>(null)
    const [error, setError] = useState<string | null>(null)

    // Determine which cards to show based on role
    const getVisibleCards = (role: string | null) => {
        const roleCardsMap: Record<string, string[]> = {
            executive: ['trustScore', 'spiderChart', 'keyTakeaways', 'alternatives'],
            security: ['vulnerabilities', 'incidents', 'recentCVEs', 'recentIncidents'],
            compliance: ['certifications', 'compliance'],
            technical: ['architecture'],
            global: ['trustScore', 'spiderChart', 'vulnerabilities', 'incidents', 'recentCVEs', 'recentIncidents', 'keyTakeaways', 'architecture', 'certifications', 'compliance', 'alternatives']
        }

        const normalizedRole = role?.toLowerCase() || 'global'
        const allowedCards = roleCardsMap[normalizedRole] || roleCardsMap.global

        return {
            trustScore: allowedCards.includes('trustScore'),
            spiderChart: allowedCards.includes('spiderChart'),
            vulnerabilities: allowedCards.includes('vulnerabilities'),
            incidents: allowedCards.includes('incidents'),
            recentCVEs: allowedCards.includes('recentCVEs'),
            recentIncidents: allowedCards.includes('recentIncidents'),
            keyTakeaways: allowedCards.includes('keyTakeaways'),
            architecture: allowedCards.includes('architecture'),
            certifications: allowedCards.includes('certifications'),
            compliance: allowedCards.includes('compliance'),
            alternatives: allowedCards.includes('alternatives'),
        }
    }

    const visibleCards = getVisibleCards(role)

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
        <div className="animate-fade-in w-full max-w-5xl">
            <h2 className="text-2xl sm:text-3xl font-medium text-gray-900 dark:text-white mb-4 sm:mb-6 text-center">
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

            {/* All other cards - Responsive Grid Layout */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {visibleCards.trustScore && (
                    <div>
                        <TrustScoreCard
                            score={assessment.summary.trust_score.score}
                            confidence={assessment.summary.trust_score.confidence}
                        />
                    </div>
                )}
                {visibleCards.spiderChart && (
                    <div>
                        <SpiderChartCard data={assessment.summary.trust_score}/>
                    </div>
                )}
                {visibleCards.vulnerabilities && (
                    <div>
                        <VulnerabilitiesCard cves={assessment.cves}/>
                    </div>
                )}
                {visibleCards.incidents && (
                    <div>
                        <IncidentsCard incidents={assessment.incidents}/>
                    </div>
                )}
                {visibleCards.recentCVEs && (
                    <div className="md:col-span-2">
                        <RecentCVEsCard cves={assessment.cve.critical} />
                    </div>
                )}
                {visibleCards.recentIncidents && (
                    <div className="md:col-span-2">
                        <RecentIncidentsCard incidents={assessment.incident.items} />
                    </div>
                )}
                {visibleCards.keyTakeaways && (
                    <div>
                        <KeyTakeawaysCard
                            strengths={assessment.summary.key_strengths}
                            risks={assessment.summary.key_risks}
                        />
                    </div>
                )}
                {visibleCards.architecture && (
                    <div>
                        <ArchitectureCard architecture={assessment.architecture}/>
                    </div>
                )}
                {visibleCards.certifications && (
                    <div>
                        <CertificationsCard certs={assessment.compliance.certs}/>
                    </div>
                )}
                {visibleCards.compliance && (
                    <div>
                        <ComplianceCard
                            frameworks={assessment.compliance.frameworks}
                            data_residency={assessment.compliance.data_residency}
                        />
                    </div>
                )}
                {visibleCards.alternatives && (
                    <div>
                        <AlternativesCard
                            alternatives={assessment.alternatives.items}
                            currentRole={role || 'global'}
                        />
                    </div>
                )}
            </div>
        </div>
    )
}
