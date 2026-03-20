from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt  # jose library for encoding/decoding JWTs
from passlib.context import CryptContext  # passlib for password hashing

from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

# --------------------------
# Password hashing
# --------------------------

# Create a password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plaintext password against a hashed password.
        Returns True if they match, False otherwise.
        Example usage:
        Usuario escribe: "123456"
        Tú comparas con el hash guardado
        Devuelve True o False
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a plaintext password using bcrypt.
        Returns the hashed password as a string.
        Exameple usage:
        "123456" -> "$2b$12$KIXQJj8uG9Z5e5s1z1e7uO8v1X9f5a6b7c8d9e0f1g2h3i4j5k6l7m8n9o0p"
        """
        return pwd_context.hash(password)


# --------------------------
# JWT Settings
# --------------------------


SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in environment variables")

ALGORITHM = "HS256"                   # Algorithm used to sign the token
ACCESS_TOKEN_EXPIRE_MINUTES = 60      # Token expiration time (minutes)


# --------------------------
# JWT Functions
# --------------------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a JWT access token for a user.

    Parameters:
    - data: dictionary containing information to encode in the token (e.g., {"sub": username})
    - expires_delta: optional timedelta for token expiration. If None, defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
    - encoded JWT token as a string
    """
    to_encode = data.copy()  # Copy the data to avoid modifying the original
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # Add the expiration timestamp to the payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the token
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode a JWT token and return its payload.

    Parameters:
    - token: JWT token string to decode

    Returns:
    - dictionary containing token payload

    Raises:
    - JWTError if the token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode and verify token
        return payload
    except JWTError:
        # Raise an error if the token is invalid or expired
        raise JWTError("Invalid or expired token")