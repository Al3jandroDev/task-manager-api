from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.models.task import Task


from typing import Annotated
from app.db.database import get_session  # tu dependencia de sesión
from app.services.auth import get_current_user
SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)



# POST /tasks/ crear tarea
@router.post("/", response_model=TaskRead, status_code=201)
def create_task(task_create: TaskCreate, session: SessionDep,
                current_user: User = Depends(get_current_user)):
    

    if not task_create.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty"
        )
        
    new_task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        owner_id=current_user.id
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


# GET tasks/ ver tareas
@router.get("/", response_model=list[TaskRead])
def read_tasks(session: SessionDep,
            current_user: User = Depends(get_current_user)):
    statement = select(Task).where(Task.owner_id == current_user.id)
    tasks = session.exec(statement).all()
    return tasks

# GET  /tasks/{id} ver una
@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: int, session: SessionDep,
            current_user: User = Depends(get_current_user)):
    
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    
    return task


# PUT  /tasks/{id} actualizar
@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_update: TaskUpdate, session: SessionDep,
                current_user: User = Depends(get_current_user)):
    
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    update_data = task_update.dict(exclude_unset=True)  # solo los que llegaron
    for field, value in update_data.items():
        if field == "title" and (value is None or not value.strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty"
            )
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


# DELETE /tasks/{id}  borrar
@router.delete("/{task_id}")
def delete_task(task_id: int, session: SessionDep,
                current_user: User = Depends(get_current_user)):
    
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    session.delete(task)
    session.commit()

    return {"detail": "Task deleted successfully", "id": task.id}


