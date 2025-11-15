"""Assessment data models."""
from typing import List, Optional, TYPE_CHECKING
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, JSON

if TYPE_CHECKING:
    from .application import Application
    from .vendor import Vendor


class Levels(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class CVETrend(SQLModel, table=True):
    """CVE trend information."""
    id: Optional[int] = Field(default=None, primary_key=True)
    assessment_id: Optional[int] = Field(default=None, foreign_key="assessment.id")
    cve_id: str
    severity: Levels
    description: str
    published_date: Optional[str] = None
    sources: List[str] = Field(default_factory=list,sa_column=Column(JSON))

    # Relationship
    assessment: Optional["Assessment"] = Relationship(back_populates="cve_trends")


class ComplianceSignal(SQLModel, table=True):
    """Compliance signal information."""
    id: Optional[int] = Field(default=None, primary_key=True)
    assessment_id: Optional[int] = Field(default=None, foreign_key="assessment.id")
    framework: str  # e.g., "SOC2", "ISO27001", "GDPR"
    status: str  # e.g., "Compliant", "Partial", "Unknown"
    details: Optional[str] = None
    sources: List[str] = Field(default_factory=list,sa_column=Column(JSON))

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
    sources: List[str] = Field(default_factory=list,sa_column=Column(JSON))

    # Relationships
    assessment: Optional["Assessment"] = Relationship(back_populates="safer_alternatives")
    vendor: Optional["Vendor"] = Relationship()
    
class SecurityControls(SQLModel, table=True):
    """Security controls information."""
    id: Optional[int] = Field(default=None, primary_key=True)
    assessment_id: Optional[int] = Field(default=None, foreign_key="assessment.id")
    control_name: str
    implemented: bool
    details: Optional[str] = None
    sources: List[str] = Field(default_factory=list,sa_column=Column(JSON))

    # Relationship
    assessment: Optional["Assessment"] = Relationship(back_populates="security_controls")
    
class RiskWeaknessResidualExposure(SQLModel, table=True):
    """Risk, Weakness, and Residual Exposure information."""
    id: Optional[int] = Field(default=None, primary_key=True)
    assessment_id: Optional[int] = Field(default=None, foreign_key="assessment.id")
    risk_name: str
    description: str
    severity: Levels  # e.g., "Low", "Medium", "High"
    mitigation: Optional[str] = None
    sources: List[str] = Field(default_factory=list,sa_column=Column(JSON))

    # Relationship
    assessment: Optional["Assessment"] = Relationship(back_populates="risk_weakness_residual_exposures")
    



class Assessment(SQLModel, table=True):
    """Complete security assessment for a tool/application."""
    id: Optional[int] = Field(default=None, primary_key=True)
    vendor_id: Optional[int] = Field(default=None, foreign_key="vendor.id")
    application_id: Optional[int] = Field(default=None, foreign_key="application.id")
    
    # Relationships
    vendor: Optional["Vendor"] = Relationship()
    application: Optional["Application"] = Relationship()
    cve_trends: List["CVETrend"] = Relationship(back_populates="assessment")
    compliance_signals: List["ComplianceSignal"] = Relationship(back_populates="assessment")
    safer_alternatives: List["Alternative"] = Relationship(back_populates="assessment")
    security_controls: List["SecurityControls"] = Relationship(back_populates="assessment")
    risk_weakness_residual_exposures: List["RiskWeaknessResidualExposure"] = Relationship(back_populates="assessment")
    trust_score: float = Field(default=0.0, description="Overall trust score of the application")
    confidence_level: Levels = Field(default=Levels.low, description="Confidence level of the assessment")

    def to_json(self) -> dict:
        """Convert to JSON-serializable dict."""
        return self.model_dump()
