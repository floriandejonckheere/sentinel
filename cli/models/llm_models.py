from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class SeverityLevel(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"
    
class TrustTrend(str, Enum):
    improving = "improving"
    degrading = "degrading"
    stable = "stable"
    
class TrustConfidence(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    
class CVECounts(BaseModel):
    total: int = Field(..., ge=0)
    critical: int = Field(..., ge=0)
    high: int = Field(..., ge=0)
    medium: int = Field(..., ge=0)
    low: int = Field(..., ge=0)
    trend: TrustTrend = Field(
        ...,
        description="CVE posture trend (e.g., improving, stable, degrading).",
    )

class LLMComplianceSignal(BaseModel):
    framework: str = Field(..., description="e.g., ISO27001, SOC2, GDPR",)
    status: str = Field(..., description="Compliant | Partial | Unknown | Noncompliant")
    details: str = Field(..., description="Evidence summary and key gaps")
    audit_reports: List[str] = Field(..., description="List of available audit reports", default_factory=list)
    sources: List[str] = Field(..., description="URLs or doc refs cited for this signal", default_factory=list)
    
class LLMComplianceSignalList(BaseModel):
    signals: List[LLMComplianceSignal] = Field(..., min_items=1)
    
from typing import List, Optional
from pydantic import BaseModel, Field


class VendorIntel(BaseModel):
    """Company background and reputation."""

    # Core identification
    name: str = Field(..., description="The official vendor or product name (brand name).")
    legal_name: str = Field(
        ...,
        description="Vendor legal entity name"
                    "(e.g., 'AgileBits Inc.').",
    )

    # Location and size
    country: Optional[str] = Field(
        None,
        description="Country of headquarters or primary operation (e.g., 'Canada').",
    )
    size: Optional[str] = Field(
        None,
        description="Organization size (e.g., '500 employees', 'Enterprise', 'Startup').",
    )

    # Web presence
    url: Optional[str] = Field(
        None,
        description="Canonical website URL of the vendor or main product (e.g., 'https://1password.com').",
    )

    # Reputation / intel
    notable_customers: List[str] = Field(
        default_factory=list,
        description="Known or publicly listed customers and partners.",
    )
    security_team: Optional[str] = Field(
        None,
        description="Information about the vendor’s security or trust team (names, roles, or presence).",
    )

    # Provenance
    sources: List[str] = Field(
        default_factory=list,
        description="URLs used to derive this information.",
    )

class ApplicationIntel(BaseModel):
    name: str = Field(..., description="The official name of the application or product.")
    description: Optional[str] = Field(None, description="A brief description of the application or product.")

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
    """Single compliance certification assesment."""
    type: str = Field(..., description="Certification (e.g., ISO 27001, SOC 2 Type II).")
    status: str = Field(..., description="Status or outcome (e.g., Certified, In Progress, Claimed, Expired).")
    year: Optional[int] = Field(None, description="Year the certification was issued or last audited.")
    issued_by: Optional[str] = Field(None, description="Issuing body or certification authority (e.g., 'A-LIGN', 'BSI').")
    issue_date: Optional[str] = Field(None, description="Date when the certification was issued.")
    expiration_date: Optional[str] = Field(None, description="Date when the certification expires or was last valid.")
    scope: Optional[str] = Field(None, description="Scope or environment covered (e.g., 'production systems', 'EU region', etc.).")
    auditor: Optional[str] = Field(None, description="Auditor or certification body (e.g., 'EY', 'A-LIGN', 'BSI').")
    report_url: Optional[str] = Field(None, description="Direct link to the attestation report or summary, if available.")
    standards: List[str] = Field(default_factory=list, description="Associated standards, controls, or trust principles (e.g., ISO 27001 Annex A, SOC 2 CC1–CC9).")
    summary: Optional[str] = Field(None, description="Brief summary of certification content or findings.")
    sources: List[str] = Field(default_factory=list, description="URLs or documents cited to identify this certification.")
    
class ComplianceFramework(BaseModel):
    """Single compliance framework assesment."""
    type: str = Field(..., description="Framework (e.g., SOC 2, ISO27001, GDPR, HIPAA, FedRAMP).")
    compliance_level: str = Field(..., description="Compliance status (e.g., Compliant, Partial, Unknown, Noncompliant).")
    year: Optional[int] = Field(None, description="Year the certification was issued or last audited.")
    last_audit_date: Optional[str] = Field(None, description="Date when the last audit was conducted.")
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
    data_residency: Optional[str] = Field(
        None,       
        description="Data residency (e.g., 'US', 'EU', 'Global').",
    )


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
    trend: TrustTrend = Field(..., description="Overall incident trend (Improving, Degrading, or Stable).")
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
    "Security",
    "Developer Tools",
    "Productivity",
    "Communication & Collaboration",
    "Multimedia & Creative",
    "File Transfer / Remote Access / Network",
    "System Utilities",
    "Virtualization & Emulation",
    "Input Method Editors (IME)",
]

ALLOWED_SUBCATEGORIES = [
    # Security
    "Password Manager",
    "Client-Side Encryption",
    "Disk Encryption",
    "Security Suite",
    "Anti-Malware",
    "Adware Removal",
    "System Cleanup Utility",

    # Developer Tools
    "API Client / Developer Tool",
    "Code Editor",
    "HTTP Debugging Proxy",
    "Game Engine",
    "Application Development Platform",

    # Productivity
    "Office Suite",
    "Document Management",
    "Reference Manager",
    "Business Productivity App",
    "ERP / Business Management Software",
    "Scientific Graphing / Data Analysis",

    # Communication & Collaboration
    "Messaging / Collaboration",
    "VoIP / Video Calling",
    "Video Conferencing",
    "Cloud Storage / File Sync",

    # Multimedia & Creative
    "Screen Recording",
    "Video Conversion",
    "Video Editing",
    "Screen Capture",
    "Image Editing",
    "Media Player",
    "Streaming & Recording",

    # File Transfer / Remote Access / Network
    "FTP/SFTP Client",
    "File Copy Acceleration Utility",
    "Remote Desktop / Remote Support",
    "Terminal Emulator",
    "SSH Client",

    # System Utilities
    "File Compression / Archiving",
    "File Manager",
    "Local Search Utility",
    "File Indexing & Search",
    "Uninstaller",
    "Disk Cleanup Utility",
    "System Information",

    # Virtualization & Emulation
    "Virtualization Platform",
    "Emulator / Virtualization Engine",

    # Input Method Editors (IME)
    "Input Method Editor",
]


class AppCategoryResult(BaseModel):
    """Two-level classification output for a vendor/product."""
    
    application_intel: ApplicationIntel = Field(..., description="Application information including name and description.")

    category: str = Field(
        ...,
        description=(
            "Top-level taxonomy category (e.g., 'Security', 'Productivity'). Must be one of ALLOWED_CATEGORIES."
        ),
    )
    subcategory: str = Field(
        ...,
        description=(
            "Specific subcategory within the chosen category (e.g., 'Password Manager'). Must be one of ALLOWED_SUBCATEGORIES."
        ),
    )
    url: Optional[str] = Field(None, description="Product landing page URL.")

    @field_validator("category")
    @classmethod
    def _validate_category(cls, v: str) -> str:
        if v not in ALLOWED_CATEGORIES:
            raise ValueError(f"Invalid category '{v}'. Must be one of: {', '.join(ALLOWED_CATEGORIES)}")
        return v

    @field_validator("subcategory")
    @classmethod
    def _validate_subcategory(cls, v: str) -> str:
        if v not in ALLOWED_SUBCATEGORIES:
            raise ValueError(f"Invalid subcategory '{v}'. Must be one of: {', '.join(ALLOWED_SUBCATEGORIES)}")
        return v
    
class AssessmentMetadata(BaseModel):
    """Metadata about when/how the assessment was generated."""

    assessed_at: str = Field(
        ..., description="ISO-8601 timestamp when this assessment was generated."
    )
    
class IncidentCounts(BaseModel):
    """Roll-up of incident counts for the assessed vendor/product."""

    total: int = Field(..., ge=0)
    critical: int = Field(..., ge=0)
    high: int = Field(..., ge=0)
    medium: int = Field(..., ge=0)
    low: int = Field(..., ge=0)
    trend: TrustTrend = Field(
        ...,
        description="Trend of incident posture (e.g., improving, stable, degrading).",
    )
    
class ArchitectureSummary(BaseModel):
    """Headline cryptographic and deployment architecture summary."""

    encryption: Optional[str] = Field(
        None, description="Primary encryption scheme(s) used (e.g., AES-256-GCM)."
    )
    key_derivation: Optional[str] = Field(
        None, description="Key derivation function(s) (e.g., PBKDF2-HMAC-SHA256)."
    )
    zero_knowledge: Optional[bool] = Field(
        None, description="Whether the service follows a zero-knowledge model."
    )
    open_source: Optional[bool] = Field(
        None, description="Whether core components are open source."
    )
    authentication: Optional[str] = Field(
        None, description="Headline authentication mechanisms (MFA, SSO, biometric, etc.)."
    )
    deployment: Optional[str] = Field(
        None, description="Primary deployment model (e.g., saas, on-prem, hybrid)."
    )
    
class TrustScoreBreakdown(BaseModel):
    score: int
    confidence: TrustConfidence
    trend: TrustTrend

    architecture: int
    data_protection: int
    identity_access: int
    devsecops: int
    historical_security: int
    compliance: int
    platform_security: int
    risks_exposure: int
    
class AssessmentSummary(BaseModel):
    """High-level summary for human consumption."""

    trust_score: Optional[TrustScoreBreakdown] = Field(
        None, description="Aggregated trust and security score breakdown."
    )
    key_strengths: List[str] = Field(
        default_factory=list,
        description="Bullet points describing the strongest security attributes.",
    )
    key_risks: List[str] = Field(
        default_factory=list,
        description="Bullet points describing the main risks or concerns.",
    )
    
class Alternative(BaseModel):
    """Alternative safer tool recommendation."""
    name: str
    risk_score: Optional[float] = None
    reason: str  # Why this is a safer alternative
    sources: List[str] = Field(default_factory=list, description="URLs or documents cited for this alternative.")

class Alternatives(BaseModel):
    items: List[Alternative] = Field(..., description="List of safer alternative tools recommended")


class ResearchReport(BaseModel):
    """Comprehensive security research report combining all agent outputs."""
    vendor: VendorIntel = Field(..., description="Vendor Intelligence section: background and reputation.")
    category: AppCategoryResult = Field(..., description="Product category and subcategory classification result.")
    cve: CVESection = Field(..., description="CVE and vulnerability history.")
    compliance: ComplianceSection = Field(..., description="Compliance and certification posture.")
    incidents: IncidentSection = Field(..., description="Security incidents and breach history.")
    docs: DocFeatures = Field(..., description="Security features extracted from documentation.")
    
class StrenghtsAndRisks(BaseModel):
    """Concise strengths and risks summary."""
    key_strengths: List[str] = Field(
        default_factory=list,
        description="Bullet points describing the strongest security attributes.",
    )
    key_risks: List[str] = Field(
        default_factory=list,
        description="Bullet points describing the main risks or concerns.",
    )

class FullAssesment(BaseModel):
    id: Optional[int] = Field(
        None, description="Internal numeric identifier for this assessment."
    )
    metadata: AssessmentMetadata = Field(
        ..., description="Metadata about assessment timing and generation."
    )
    vendor: VendorIntel = Field(
        ..., description="Vendor profile with basic and extended intel."
    )
    cve: CVESection = Field(
        ..., description="Detailed CVE and vulnerability history section."
    )
    cves: CVECounts = Field(
        ..., description="Aggregated CVE counts and trend for the vendor/product."
    )
    incidents: IncidentCounts = Field(
        ..., description="Aggregated incident counts and trend."
    )
    incident: IncidentSection = Field(
        ..., description="Detailed incident and breach history section."
    )
    architecture: ArchitectureSummary = Field(
        ..., description="Key architectural properties relevant to security."
    )
    compliance: ComplianceSection = Field(
        ..., description="Condensed view of compliance and data residency."
    )
    
    application: AppCategoryResult = Field(
        ..., description="Product category and subcategory classification."
    )
    
    alternatives: Alternatives = Field(
        ..., description="List of recommended safer alternative tools."
    )
    summary: AssessmentSummary = Field(
        ..., description="High-level assessment summary and trust score."
    )