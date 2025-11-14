"""Assessment data models."""
from pydantic import BaseModel, Field

class Application(BaseModel):
    """Application information."""
    name: str = Field(description="Name of the application")
    url: str = Field(description="Official URL of the application")