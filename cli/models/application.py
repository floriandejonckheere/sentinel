"""Assessment data models."""
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

from .vendor import Vendor


class Application(SQLModel, table=True):
    """Application information."""
    id: Optional[int] = Field(default=None, primary_key=True)
    vendor_id: Optional[int] = Field(default=None, foreign_key="vendor.id")
    name: str = Field(description="Name of the application")
    description: str = Field(description="Brief description of the application")
    url: str = Field(description="Official URL of the application")
    category: str = Field(description="Category of the application")
    subcategory: str = Field(description="Subcategory of the application")

    # Relationship
    vendor: Optional[Vendor] = Relationship()
