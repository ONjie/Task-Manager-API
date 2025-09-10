from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.schemas.schemas import TaskCreate, TaskRead, TaskUpdate, UserRead
from app.auth.auth import get_current_user
from app.database.database import get_db
from app.crud.task_crud import create_task, get_tasks, get_task, update_task, delete_task
from app.exceptions.exceptions import TaskNotFoundException


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(task:TaskCreate, current_user: Annotated[UserRead, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
  return create_task(task=task, owner_id=current_user.id, db=db)

@router.get("/", response_model=List[TaskRead])
async def read_tasks_endpoint( 
    current_user: Annotated[UserRead, Depends(get_current_user)], 
    db: Annotated[Session, Depends(get_db)],
    status_filter: Optional[bool] = Query(None, description="Filter by status: true/false"),
    q: Optional[str] = Query(None, description="Search in title/description"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    ):
  try:
     return  get_tasks(
       owner_id=current_user.id, 
       db=db, 
       status_filter=status_filter, 
       q=q, 
       limit=limit, 
       offset=offset
       )
  except TaskNotFoundException as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
  

@router.get("/{task_id}", response_model=TaskRead)
async def read_task_endpoint( 
    current_user: Annotated[UserRead, Depends(get_current_user)], 
    db: Annotated[Session, Depends(get_db)],
    task_id: int
    ):
  try:
     return  get_task(
       owner_id=current_user.id, 
       db=db, 
       task_id=task_id
       )
  except TaskNotFoundException as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

@router.put("/{task_id}", response_model=TaskRead)
async def update_task_endpoint( 
    current_user: Annotated[UserRead, Depends(get_current_user)], 
    db: Annotated[Session, Depends(get_db)],
    task_id: int,
    task: TaskUpdate
    ):
  try:
     return  update_task(
       owner_id=current_user.id, 
       db=db, 
       task_id=task_id,
       task=task
       )
  except TaskNotFoundException as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint( 
    current_user: Annotated[UserRead, Depends(get_current_user)], 
    db: Annotated[Session, Depends(get_db)],
    task_id: int,
    ):
  try:
     return delete_task(
       owner_id=current_user.id, 
       db=db, 
       task_id=task_id,
       )
  except TaskNotFoundException as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)



