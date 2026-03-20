from pydantic import BaseModel, EmailStr

# Schema for creating users (registration)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Plain text password, will be hashed before storing

# Schema for returning users (safe data)
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

# Schema for login
class UserLogin(BaseModel):
    username: str  # or email: str if you want login via email
    password: str