# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.schemas.user import UserCreate, UserRead, UserLogin
from app.models.user import User
from app.services.auth import Hasher, create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

from typing import Annotated
from sqlmodel import Session
from app.db.database import get_session  # tu dependencia de sesión

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SessionDep = Annotated[Session, Depends(get_session)]

# -----------------------------
# REGISTER endpoint
# -----------------------------
@router.post("/register", response_model=UserRead)
def register(user_create: UserCreate, session: SessionDep):
    """
    Endpoint to register a new user.
    Steps:
    1. Check if username or email already exists.
    2. Hash the password using Hasher.
    3. Save the user in the database.
    4. Return the safe UserRead object.
    """
    # Check if username or email already exists
    statement = select(User).where(
        (User.username == user_create.username) | (User.email == user_create.email)
    )
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Hash the password
    hashed_password = Hasher.get_password_hash(user_create.password)

    # Create User object
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        password_hash=hashed_password
    )

    # Save to DB
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user  # Pydantic UserRead hides password_hash automatically


# -----------------------------
# LOGIN endpoint
# -----------------------------
@router.post("/login")
def login(user_login: UserLogin, session: SessionDep):
    """
    Endpoint to login a user.
    Steps:
    1. Find user by username (or email).
    2. Verify password using Hasher.verify_password().
    3. Generate JWT token if credentials are correct.
    """
    statement = select(User).where(User.username == user_login.username)
    user = session.exec(statement).first()

    if not user or not Hasher.verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Generate JWT token
    token_data = {"sub": user.username}
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}