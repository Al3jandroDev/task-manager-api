from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True, unique=True)
    completed: bool = Field(default=False)
    owner_id: int = Field(foreign_key="user.id")

