"""Assessment data models."""
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .application import Application
    from .vendor import Vendor


class CVETrend(SQLModel, table=True):
    """CVE trend information."""
    id: Optional[int] = Field(default=None, primary_key=True)
    assessment_id: Optional[int] = Field(default=None, foreign_key="assessment.id")
    cve_id: str
    severity: str
    description: str
    published_date: Optional[str] = None

    # Relationship
    assessment: Optional["Assessment"] = Relationship(back_populates="cve_trends")


class ComplianceSignal(SQLModel, table=True):
    """Compliance signal information."""
    id: Optional[int] = Field(default=None, primary_key=True)
    assessment_id: Optional[int] = Field(default=None, foreign_key="assessment.id")
    framework: str  # e.g., "SOC2", "ISO27001", "GDPR"
    status: str  # e.g., "Compliant", "Partial", "Unknown"
    details: Optional[str] = None

    # Relationship
    assessment: Optional["Assessment"] = Relationship(back_populates="compliance_signals")


class Alternative(SQLModel, table=True):
    """Safer alternative tool."""
    id: Optional[int] = Field(default=None, primary_key=True)
    assessment_id: Optional[int] = Field(default=None, foreign_key="assessment.id")
    vendor_id: Optional[int] = Field(default=None, foreign_key="vendor.id")
    name: str
    risk_score: float
    reason: str  # Why this is a safer alternative

    # Relationships
    assessment: Optional["Assessment"] = Relationship(back_populates="safer_alternatives")
    vendor: Optional["Vendor"] = Relationship()


class Assessment(SQLModel, table=True):
    """Complete security assessment for a tool/application."""
    id: Optional[int] = Field(default=None, primary_key=True)
    vendor_id: Optional[int] = Field(default=None, foreign_key="vendor.id")
    application_id: Optional[int] = Field(default=None, foreign_key="application.id")
    risk_score: float = Field(ge=0.0, le=10.0, description="Risk score from 0 (safest) to 10 (riskiest)")
    trust_brief: str = Field(description="CISO-ready trust brief summary")

    # Relationships
    vendor: Optional["Vendor"] = Relationship()
    application: Optional["Application"] = Relationship()
    cve_trends: List["CVETrend"] = Relationship(back_populates="assessment")
    compliance_signals: List["ComplianceSignal"] = Relationship(back_populates="assessment")
    safer_alternatives: List["Alternative"] = Relationship(back_populates="assessment")

    def to_json(self) -> dict:
        """Convert to JSON-serializable dict."""
        return self.model_dump()
