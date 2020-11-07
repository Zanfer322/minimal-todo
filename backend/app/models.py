from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel


class TodoState(str, Enum):
    ongoing = "ongoing"
    done = "done"
    cancelled = "cancelled"


class Todo(BaseModel):
    id: str
    contents: str
    state: TodoState
    created_at: datetime
    updated_at: datetime
    state_updated_at: datetime
    tags: List["Tag"]


class Tag(BaseModel):
    id: str
    name: str
    created_at: datetime
