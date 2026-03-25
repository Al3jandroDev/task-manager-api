from sqlmodel import Session, select
from app.models.user import User

def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()