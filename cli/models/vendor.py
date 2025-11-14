"""Assessment data models."""
from typing import Optional
from sqlmodel import Field, SQLModel


class Vendor(SQLModel, table=True):
    """Vendor/company information."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(description="Common/brand name of the vendor")
    legal_name: str = Field(description="Legal/registered company name")
    country: str = Field(description="Country of incorporation/headquarters")
    url: str = Field(description="Official website URL")
