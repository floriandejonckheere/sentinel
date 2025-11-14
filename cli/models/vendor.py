"""Assessment data models."""
from pydantic import BaseModel, Field

class Vendor(BaseModel):
    """Vendor/company information."""
    name: str = Field(description="Common/brand name of the vendor")
    legal_name: str = Field(description="Legal/registered company name")
    country: str = Field(description="Country of incorporation/headquarters")
    url: str = Field(description="Official website URL")