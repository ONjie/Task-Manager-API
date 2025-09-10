from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str
    status: Optional[bool] = False

class TaskCreate(TaskBase):
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = False 
    due_date: Optional[datetime] = None


class TaskRead(TaskBase):
    id: int
    due_date: datetime

    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    tasks: List[TaskRead] = []

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None


class RefreshRequest(BaseModel):
    refresh_token: str