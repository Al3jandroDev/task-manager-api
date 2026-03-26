from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    """
    Task model representing a to-do item in the system.
    Each task is linked to a specific user (owner).
    """

    # Unique identifier for each task (Primary Key)
    id: int | None = Field(default=None, primary_key=True)

    # Title of the task (indexed for faster search)
    title: str = Field(index=True)

    # Task description (must be unique across all tasks)
    description: str = Field(index=True, unique=True)

    # Indicates whether the task is completed or not
    completed: bool = Field(default=False)

    # Foreign key linking the task to its owner (User)
    owner_id: int = Field(foreign_key="user.id")

