from pydantic import BaseModel, EmailStr

# CREATE USER (REGISTER)
class UserCreate(BaseModel):
    """
    Schema used for user registration.
    Accepts raw user input (including plain password).
    """
    username: str
    email: EmailStr  # Validates correct email format
    password: str  # Plain text password (will be hashed before storing)

# READ USER (RESPONSE)
class UserRead(BaseModel):
    """
    Schema used to return user data safely.
    Excludes sensitive information such as password hash.
    """
    id: int
    username: str
    email: EmailStr

    class Config:
        # Enables compatibility with ORM models (SQLModel)
        from_attributes = True

# LOGIN SCHEMA
class UserLogin(BaseModel):
    """
    Schema used for user authentication.
    Accepts login credentials.
    """
    username: str   # Can be replaced with email if needed
    password: str