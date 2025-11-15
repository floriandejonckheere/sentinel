from typing import List
from pydantic import BaseModel, Field


class LLMComplianceSignal(BaseModel):
    framework: str = Field(..., description="e.g., ISO27001, SOC2, GDPR")
    status: str = Field(..., description="Compliant | Partial | Unknown | Noncompliant")
    details: str = Field(..., description="Evidence summary and key gaps")
    sources: List[str] = Field(..., description="URLs or doc refs cited for this signal")
    
class LLMComplianceSignalList(BaseModel):
    signals: List[LLMComplianceSignal] = Field(..., min_items=1)