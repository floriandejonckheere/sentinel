from enum import Enum
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"

class LLMComplianceSignal(BaseModel):
    framework: str = Field(..., description="e.g., ISO27001, SOC2, GDPR",)
    status: str = Field(..., description="Compliant | Partial | Unknown | Noncompliant")
    details: str = Field(..., description="Evidence summary and key gaps")
    audit_reports: List[str] = Field(..., description="List of available audit reports", default_factory=list)
    sources: List[str] = Field(..., description="URLs or doc refs cited for this signal", default_factory=list)
    
class LLMComplianceSignalList(BaseModel):
    signals: List[LLMComplianceSignal] = Field(..., min_items=1)
    
class VendorIntel(BaseModel):
    """Company background and reputation."""
    name: str = Field(..., description="The official vendor or product name.")
    country: Optional[str] = Field(None, description="Country of headquarters or primary operation.")
    size: Optional[str] = Field(None, description="Organization size (e.g., '500 employees', 'Enterprise', 'Startup').")
    notable_customers: List[str] = Field(
        default_factory=list,
        description="Known or publicly listed customers and partners."
    )
    security_team: Optional[str] = Field(
        None, description="Information about the vendor’s security or trust team (names, roles, or presence)."
    )
    sources: List[str] = Field(
        default_factory=list,
        description="URLs used to derive this information."
    )
    website: str = Field(None, description="Official website URL of the vendor or product.")

class CVEItem(BaseModel):
    """Individual vulnerability record."""
    cve_id: str = Field(..., description="The CVE identifier (e.g., CVE-2025-1234).")
    severity: Optional[SeverityLevel] = Field(None, description="Vulnerability severity (Critical, High, Medium, Low).")
    description: str = Field(..., description="Short description of the vulnerability or impact.")
    year: Optional[int] = Field(None, description="Year the CVE was published or discovered.")
    sources: List[str] = Field(default_factory=list, description="Cited URLs or advisories for this CVE.")


class CVESection(BaseModel):
    """Summary of vulnerability history and trends."""
    by_year_counts: Dict[str, int] = Field(
        default_factory=dict,
        description="Counts of CVEs by year, e.g., {'2023': 12, '2024': 9}."
    )
    critical: List[CVEItem] = Field(
        default_factory=list,
        description="List of critical or notable CVEs associated with the vendor."
    )
    trend: str = Field(..., description="Overall vulnerability trend (Improving, Degrading, or Stable).")
    summary: str = Field(..., description="Paragraph summarizing vulnerability history and exposure trends.")
    sources: List[str] = Field(default_factory=list, description="Sources used for vulnerability research.")

class ComplianceCert(BaseModel):
    """Single compliance certification or attestation."""
    framework: str = Field(..., description="Framework or standard name (e.g., SOC 2 Type II, ISO/IEC 27001:2022, PCI DSS 4.0).")
    status: str = Field(..., description="Status or outcome (e.g., Certified, In Progress, Claimed, Expired).")
    year: Optional[int] = Field(None, description="Year the certification was issued or last audited.")
    scope: Optional[str] = Field(None, description="Scope or environment covered (e.g., 'production systems', 'EU region', etc.).")
    auditor: Optional[str] = Field(None, description="Auditor or certification body (e.g., 'EY', 'A-LIGN', 'BSI').")
    report_url: Optional[str] = Field(None, description="Direct link to the attestation report or summary, if available.")
    standards: List[str] = Field(default_factory=list, description="Associated standards, controls, or trust principles (e.g., ISO 27001 Annex A, SOC 2 CC1–CC9).")
    summary: Optional[str] = Field(None, description="Brief summary of certification content or findings.")
    sources: List[str] = Field(default_factory=list, description="URLs or documents cited to identify this certification.")
    
class ComplianceSection(BaseModel):
    """Section summarizing all compliance certifications and posture."""
    certs: List[ComplianceCert] = Field(..., description="List of discovered or claimed compliance certifications.")
    overall_summary: str = Field(..., description="High-level summary of compliance and audit posture across all frameworks.")
    sources: List[str] = Field(default_factory=list, description="Unique list of URLs or sources used across all certifications.")


class IncidentSignal(BaseModel):
    """Individual incident or breach report."""
    title: str = Field(..., description="Headline or title of the security incident.")
    date: Optional[str] = Field(None, description="Date or approximate time the incident occurred or was disclosed.")
    severity: Optional[SeverityLevel] = Field(
        None, description="Impact level (High, Medium, Low) or qualitative severity assessment."
    )
    description: str = Field(..., description="Brief description of the event and its implications.")
    sources: List[str] = Field(default_factory=list, description="URLs to news or official disclosures.")

class IncidentSection(BaseModel):
    """Summary of negative security signals."""
    items: List[IncidentSignal] = Field(
        default_factory=list,
        description="List of known breaches, incidents, or controversies related to the vendor."
    )
    summary: str = Field(..., description="Overall assessment of incident history and transparency.")
    sources: List[str] = Field(default_factory=list, description="Cited URLs and reports for incidents.")

class DocFeatures(BaseModel):
    """Extracted security and deployment features from product documentation."""
    encryption: List[str] = Field(
        default_factory=list,
        description="Details about encryption at rest/in transit, key management, and cryptographic standards."
    )
    authentication: List[str] = Field(
        default_factory=list,
        description="Supported authentication methods (e.g., MFA, SSO, SCIM, OAuth)."
    )
    data_handling: List[str] = Field(
        default_factory=list,
        description="Information about data storage, residency, retention, and deletion policies."
    )
    admin_controls: List[str] = Field(
        default_factory=list,
        description="Administrative and access controls (e.g., RBAC, audit logs, approval workflows)."
    )
    deployment_model: List[str] = Field(
        default_factory=list,
        description="Deployment or hosting options (e.g., SaaS, on-prem, hybrid, supported regions)."
    )
    summary: str = Field(..., description="Concise overview of key security features and design choices.")
    sources: List[str] = Field(default_factory=list, description="Documentation URLs or whitepapers referenced.")
    
ALLOWED_CATEGORIES = [
    "Productivity", "Communication", "Developer Tools", "Design", "Marketing", "Finance",
    "Data & Analytics", "Security", "HR & People", "Education", "Healthcare", "Sales",
    "Customer Support", "Media", "Operations", "Legal", "Creative", "AI & ML",
]

class AppCategoryResult(BaseModel):
    """
    Classification output indicating the most likely product category for a vendor,
    along with confidence and the model’s reasoning.
    """

    category: Literal[tuple(ALLOWED_CATEGORIES)] = Field(
        ...,
        description=(
            "The predicted category that best matches the vendor or product. "
            "Must be one of the predefined ALLOWED_CATEGORIES. "
            "Used by the workflow to route downstream research tasks "
            "(e.g., security checks, compliance, feature extraction)."
        ),
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description=(
            "A probability-like confidence score (0.0–1.0) representing the "
            "model’s certainty about the chosen category. "
            "Higher values indicate stronger confidence and may be used by "
            "the workflow to decide whether to trigger fallback or validation steps."
        ),
    )

    reasoning: str = Field(
        ...,
        description=(
            "Natural-language explanation of why the model selected the category. "
            "This is used for debugging and ensuring interpretability inside the workflow. "
            "It can also help downstream agents validate the categorization decision."
        ),
    )


class ResearchReport(BaseModel):
    """Comprehensive security research report combining all agent outputs."""
    vendor: VendorIntel = Field(..., description="Vendor Intelligence section: background and reputation.")
    category: AppCategoryResult = Field(..., description="Product category classification result.")
    cve: CVESection = Field(..., description="CVE and vulnerability history.")
    compliance: ComplianceSection = Field(..., description="Compliance and certification posture.")
    incidents: IncidentSection = Field(..., description="Security incidents and breach history.")
    docs: DocFeatures = Field(..., description="Security features extracted from documentation.")
