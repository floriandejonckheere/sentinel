"""Database connection handler."""
from sqlmodel import create_engine, SQLModel, Session

# Import all models to ensure they are registered with SQLModel


class Database:
    """Database connection handler."""
    def __init__(self, url: str):
        """Initialize the database connection."""
        self.url = url
        self.engine = create_engine(self.url, echo=False)

    def create_tables(self):
        """Create all tables in the database if they don't exist."""
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Get a database session."""
        return Session(self.engine)
