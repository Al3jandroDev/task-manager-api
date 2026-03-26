from sqlmodel import Session, SQLModel, create_engine, select
from app.models.user import User

# SQLite database file name
sqlite_file_name = "database.db"

# Database connection URL (SQLite in this case)
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Required for SQLite to allow usage across multiple threads (FastAPI uses async behavior)
connect_args = {"check_same_thread": False}

# Create the database engine (entry point to interact with the database)
engine = create_engine(sqlite_url, connect_args=connect_args)

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
