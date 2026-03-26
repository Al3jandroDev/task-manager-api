from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.schemas.user import UserCreate, UserRead, UserLogin
from app.models.user import User
from app.services.auth import Hasher, create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

from typing import Annotated
from sqlmodel import Session
from app.db.database import get_session  # Database session dependency

# Create router for authentication-related endpoints
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Dependency injection for database session
SessionDep = Annotated[Session, Depends(get_session)]


# REGISTER endpoint
@router.post("/register", response_model=UserRead)
def register(user_create: UserCreate, session: SessionDep):
    """
    Register a new user.

    Steps:
    1. Check if username or email already exists.
    2. Hash the user's password.
    3. Store the new user in the database.
    4. Return a safe response (without password).
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

    # Hash the password before storing it
    hashed_password = Hasher.get_password_hash(user_create.password)

    # Create new user instance
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        password_hash=hashed_password
    )

    # Save user to database
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Return user (password is excluded via schema)
    return new_user



# LOGIN endpoint
@router.post("/login")
def login(user_login: UserLogin, session: SessionDep):
    """
    Authenticate user and return JWT token.

    Steps:
    1. Retrieve user from database.
    2. Verify password using hashed value.
    3. Generate JWT token if credentials are valid.
    """

    # Find user by username
    statement = select(User).where(User.username == user_login.username)
    user = session.exec(statement).first()

    # Validate credentials
    if not user or not Hasher.verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create JWT payload (subject = username)
    token_data = {"sub": user.username}

    # Generate access token
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}