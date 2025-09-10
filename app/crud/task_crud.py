from sqlalchemy.orm import Session
from app.schemas.schemas import TaskCreate, TaskUpdate
from app.models.models import Task
from app.exceptions.exceptions import TaskNotFoundException

def create_task(task: TaskCreate, owner_id: int, db:Session):
    db_task = Task( title=task.title,
        description=task.description,
        status=task.status or False,
        owner_id=owner_id,)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(owner_id: int, 
              status_filter: bool | None, 
              q: str | None, 
              limit: int, 
              offset: int, 
              db:Session):
    query = db.query(Task).filter(Task.owner_id == owner_id)

    if not query:
        raise TaskNotFoundException(message="Tasks not found")
    if status_filter is not None:
        query = query.filter(Task.status == status_filter)
    if q:
        like = f"%{q}%"
        query = query.filter((Task.title.ilike(like)) | (Task.description.ilike(like)))
    return query.order_by(Task.id.desc()).offset(offset).limit(limit).all()


def get_task(task_id: int, owner_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()
    if not task:
        raise TaskNotFoundException(message="Task not found")
    return task

def update_task(task: TaskUpdate, task_id: int, owner_id: int, db: Session):
    db_task = get_task(task_id=task_id, owner_id=owner_id, db=db)

    update_data = task.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(task_id: int, owner_id: int, db: Session):
    db_task = get_task(task_id=task_id, owner_id=owner_id, db=db)

    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}