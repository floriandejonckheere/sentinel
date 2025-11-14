"""Assessment data models."""
from pydantic import BaseModel, Field

from .vendor import Vendor

class Application(BaseModel):
    """Application information."""
    vendor: Vendor = Field(description="Vendor information associated with the application")
    name: str = Field(description="Name of the application")
    url: str = Field(description="Official URL of the application")