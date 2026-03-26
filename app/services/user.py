from sqlmodel import Session, select
from app.models.user import User

def get_user_by_username(session: Session, username: str):
    """
    Retrieve a user from the database by username.

    Parameters:
    - session: active database session
    - username: username to search for

    Returns:
    - User object if found
    - None if no user exists with the given username
    """

    # Build SQL query to find user by username
    statement = select(User).where(User.username == username)

    # Execute query and return the first result (or None)
    return session.exec(statement).first()