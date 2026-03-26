from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.models.task import Task


from typing import Annotated
from app.db.database import get_session 
from app.services.auth import get_current_user

# Dependency for DB session
SessionDep = Annotated[Session, Depends(get_session)]

# Router for task-related endpoints
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)



# CREATE TASK
@router.post("/", response_model=TaskRead, status_code=201)
def create_task(task_create: TaskCreate, session: SessionDep,
                current_user: User = Depends(get_current_user)):
    """
    Create a new task for the authenticated user.
    """

    # Validate title is not empty
    if not task_create.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty"
        )
        
    # Create new task linked to current user
    new_task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        owner_id=current_user.id
    )

    # Save to database
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


# GET ALL TASKS
@router.get("/", response_model=list[TaskRead])
def read_tasks(session: SessionDep,
            current_user: User = Depends(get_current_user)):
    
    """
    Retrieve all tasks belonging to the authenticated user.
    """

    # Filter tasks by owner
    statement = select(Task).where(Task.owner_id == current_user.id)
    tasks = session.exec(statement).all()
    return tasks


# GET SINGLE TASK
@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: int, session: SessionDep,
            current_user: User = Depends(get_current_user)):
    
    """
    Retrieve a specific task by ID.
    Only accessible by its owner.
    """
    
    task = session.get(Task, task_id)

    # Check if task exists
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Authorization check
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    
    return task


# UPDATE TASK
@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_update: TaskUpdate, session: SessionDep,
                current_user: User = Depends(get_current_user)):
    
    """
    Update a task partially (only provided fields).
    """
    
    task = session.get(Task, task_id)

    # Check existence
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Authorization check
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    # Extract only provided fields
    update_data = task_update.dict(exclude_unset=True)

    # Apply updates dynamically
    for field, value in update_data.items():

        # Validate title if provided
        if field == "title" and (value is None or not value.strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty"
            )
        setattr(task, field, value)

    # Save changes
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


# DELETE TASK
@router.delete("/{task_id}")
def delete_task(task_id: int, session: SessionDep,
                current_user: User = Depends(get_current_user)):
    
    """
    Delete a task by ID.
    Only the owner can delete it.
    """
    
    task = session.get(Task, task_id)

    # Check existence
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Authorization check
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    # Delete task
    session.delete(task)
    session.commit()

    return {"detail": "Task deleted successfully", "id": task.id}


