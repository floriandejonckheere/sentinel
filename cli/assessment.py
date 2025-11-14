"""Assessment data models."""
from typing import List, Optional
from pydantic import BaseModel, Field

from vendor import Vendor


class CVETrend(BaseModel):
    """CVE trend information."""
    cve_id: str
    severity: str
    description: str
    published_date: Optional[str] = None


class ComplianceSignal(BaseModel):
    """Compliance signal information."""
    framework: str  # e.g., "SOC2", "ISO27001", "GDPR"
    status: str  # e.g., "Compliant", "Partial", "Unknown"
    details: Optional[str] = None


class Alternative(BaseModel):
    """Safer alternative tool."""
    name: str
    vendor: Vendor
    risk_score: float
    reason: str  # Why this is a safer alternative


class Assessment(BaseModel):
    """Complete security assessment for a tool/application."""
    name: str
    vendor: Vendor
    url: str
    risk_score: float = Field(ge=0.0, le=10.0, description="Risk score from 0 (safest) to 10 (riskiest)")
    trust_brief: str = Field(description="CISO-ready trust brief summary")
    cve_trends: List[CVETrend] = Field(default_factory=list)
    compliance_signals: List[ComplianceSignal] = Field(default_factory=list)
    safer_alternatives: List[Alternative] = Field(default_factory=list)

    def to_json(self) -> dict:
        """Convert to JSON-serializable dict."""
        return self.model_dump()
