from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt   # Library for encoding/decoding JWT tokens
from passlib.context import CryptContext # Password hashing utility

from dotenv import load_dotenv
import os

# FastAPI security dependencies for handling Authorization header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status


from sqlmodel import Session

from app.services.user import get_user_by_username


from app.db.database import get_session

# Security scheme: expects "Authorization: Bearer <token>" in the request headers
security = HTTPBearer(auto_error=True)

# GET CURRENT AUTHENTICATED USER
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """
    Extract and validate the current authenticated user from the JWT token.

    Steps:
    1. Extract token from Authorization header.
    2. Decode token payload.
    3. Retrieve user from database.
    4. Return authenticated user.
    """

    # Extract token string
    token = credentials.credentials

    try:
        # Decode JWT payload
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Extract username from token payload ("sub" = subject)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    # Retrieve user from database
    user = get_user_by_username(session, username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

# Load environment variables from .env file
load_dotenv()

# PASSWORD HASHING CONFIG

# Configure bcrypt hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    """
    Utility class for password hashing and verification.
    """

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Compare a plain password with a hashed password.

        Returns True if they match, otherwise False.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a plain password using bcrypt.

        Example:
        "123456" -> "$2b$12$..."
        """
        return pwd_context.hash(password)


# JWT CONFIGURATION

# Load secret key from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in environment variables")

# Algorithm used to sign tokens
ALGORITHM = "HS256" 

# Token expiration time (in minutes)   
ACCESS_TOKEN_EXPIRE_MINUTES = 60 

# CREATE JWT TOKEN
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a JWT access token.

    Parameters:
    - data: payload to encode (e.g., {"sub": username})
    - expires_delta: optional custom expiration time

    Returns:
    - Encoded JWT token as string
    """

    # Copy data to avoid mutation
    to_encode = data.copy()

    # Set expiration time
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # Add expiration to payload
    to_encode.update({"exp": expire})

    # Encode token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the token
    return encoded_jwt


# DECODE JWT TOKEN
def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT token.

    Parameters:
    - token: JWT string

    Returns:
    - Decoded payload (dict)

    Raises:
    - JWTError if token is invalid or expired
    """
    try:
        # Decode token and verify signature + expiration
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode and verify token
        return payload
    except JWTError:
        # Raise error if token is invalid or expired
        raise JWTError("Invalid or expired token")