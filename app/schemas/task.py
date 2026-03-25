from pydantic import BaseModel

# Schema for creating tasks
class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

# Schema for returning tasks (safe data)
class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    owner_id: int

    class Config:
        from_attributes = True

# Schema for updating tasks
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None