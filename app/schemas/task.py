from pydantic import BaseModel

# CREATE SCHEMA
class TaskCreate(BaseModel):
    """
    Schema used to validate data when creating a new task.
    Defines the expected request body from the client.
    """
    title: str
    description: str
    completed: bool = False  # Default value if not provided

# READ SCHEMA (RESPONSE)
class TaskRead(BaseModel):
    """
    Schema used to return task data to the client.
    Exposes only safe and necessary fields.
    """
    id: int
    title: str
    description: str
    completed: bool
    owner_id: int

    class Config:
        # Allows compatibility with ORM models (SQLModel)
        from_attributes = True

# UPDATE SCHEMA
class TaskUpdate(BaseModel):
    """
    Schema used for updating a task.
    All fields are optional to allow partial updates.
    """
    title: str | None = None
    description: str | None = None
    completed: bool | None = None