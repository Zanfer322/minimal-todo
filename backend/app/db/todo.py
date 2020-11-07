from datetime import datetime
from typing import List, Optional
from app import models


def create_todo(contents: str, tags: List[str]) -> models.Todo:
    pass


def update_todo(todo: models.Todo) -> models.Todo:
    pass


def get_all_todos() -> List[models.Todo]:
    pass


def get_filtered_todos(
    state: Optional[models.TodoState],
    start_time: Optional[datetime],
    end_time: Optional[datetime],
    tags: List[str],
    limit: Optional[int],
    offset: Optional[int],
) -> List[models.Todo]:
    pass


def search_todo(
    search_term: str, limit: Optional[int], offset: Optional[int]
) -> List[models.Todo]:
    pass
