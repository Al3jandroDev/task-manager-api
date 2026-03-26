from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    """
    User model representing an application user.
    Stores authentication and identification data.
    """

    # Unique identifier for each user (Primary Key)
    id: int | None = Field(default=None, primary_key=True)

    # Username (must be unique, indexed for fast lookup)
    username: str = Field(index=True, unique=True)

    # User email (must be unique, indexed for fast lookup)
    email: str = Field(index=True, unique=True)

    # Hashed password (never store plain text passwords)
    password_hash: str