from datetime import datetime
from enum import Enum
from typing import Set

from pydantic import BaseModel


class TodoState(str, Enum):
    ongoing = "ongoing"
    done = "done"
    cancelled = "cancelled"


class Todo(BaseModel):
    id: str
    contents: str
    state: TodoState
    tags: Set[str]
    created_at: datetime
    updated_at: datetime
    state_updated_at: datetime


class CreateTodo(BaseModel):
    contents: str
    tags: Set[str]


class TodoUpdate(BaseModel):
    id: str
    contents: str
    state: TodoState
    tags: Set[str]


class Tag(BaseModel):
    db_id: int
    id: str
    name: str
    created_at: datetime


class CreateTag(BaseModel):
    name: str


class APITag(BaseModel):
    id: str
    name: str
    created_at: datetime
