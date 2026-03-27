from sqlmodel import Session, SQLModel, create_engine, select
from app.models.user import User
import os

# Read the database URL from environment variables
# This allows switching between local and production databases without changing code
DATABASE_URL = os.getenv("DATABASE_URL")

# Raise an error if the environment variable is missing
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# Create the SQLAlchemy/SQLModel engine
# PostgreSQL does not require 'check_same_thread' like SQLite
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """
    Create all database tables based on the SQLModel metadata.
    This will generate tables for all models that inherit from SQLModel.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Dependency that provides a database session.
    It will be injected into routes using FastAPI Depends().

    The session is automatically closed after the request is finished.
    """
    with Session(engine) as session:
        yield session
