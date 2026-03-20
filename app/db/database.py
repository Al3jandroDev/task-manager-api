from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, SQLModel, create_engine, select

from app.models.user import User  


sqlite_file_name = "database.db" # engine will create this file if it doesn't exist
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False} # SQLite specific argument to allow multiple threads (hilos) to access the database
engine = create_engine(sqlite_url, connect_args=connect_args)


# Create the database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Dependency to get a session for the database
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


# Create the database and tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# CRUD operations for the Hero model

# Create a new user
@app.post("/users/")
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Read all users with pagination (offset and limit)
@app.get("/users/")
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

# Read a single user by ID
@app.get("/users/{user_id}")
def read_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}