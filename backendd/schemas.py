from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    points: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class ChoreCreate(BaseModel):
    title: str
    due_time: Optional[str] = None
    requires_photo: bool = False
    points_value: int = 10
    assigned_to: int


class ChoreOut(BaseModel):
    id: int
    title: str
    due_time: Optional[str]
    status: str
    requires_photo: bool
    points_value: int
    assigned_to: int

    class Config:
        from_attributes = True


class RewardCreate(BaseModel):
    title: str
    points_required: int


class RewardOut(BaseModel):
    id: int
    title: str
    points_required: int

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    title: str
    date: str
    time: Optional[str]
    visible_to: str


class EventOut(BaseModel):
    id: int
    title: str
    date: str
    time: Optional[str]
    visible_to: str

    class Config:
        from_attributes = True


class RequestCreate(BaseModel):
    message: str
    child_id: int


class RequestOut(BaseModel):
    id: int
    message: str
    status: str
    created_at: datetime
    child_id: int

    class Config:
        from_attributes = True
