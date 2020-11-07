import sqlite3
import uuid
from datetime import datetime
from typing import Any, List, Optional, Set, cast
from app import models

from .tag import get_tags_by_name
from .exceptions import DBException

_ROWS = "uuid, contents, tags, state, created_at, updated_at, state_updated_at"


def _verify_tags(conn: sqlite3.Connection, tag_names: Set[str]) -> None:
    tags = get_tags_by_name(conn, tag_names)
    found_tag_names = set([t.name for t in tags if t is not None])

    if None in tags:
        raise DBException(f"invalid tags '{tag_names - found_tag_names}'")


def _get_tag_field(tag_names: Set[str]) -> Optional[str]:
    if not len(tag_names):
        return None
    return "*".join(tag_names)


def _get_tag_names(tag_field: Optional[str]) -> Set[str]:
    if tag_field is None:
        return set()
    return set(tag_field.split("*"))


def create_todo(
    conn: sqlite3.Connection, contents: str, tag_names: Set[str]
) -> models.Todo:
    _verify_tags(conn, tag_names)

    id = uuid.uuid4().hex
    created_at = datetime.now()
    state = models.TodoState.ongoing

    conn.execute(
        f"""
        insert into
        todo({_ROWS})
        values ({', '.join(['?' for _ in _ROWS.split(',')])})
        """,
        (
            id,
            contents,
            _get_tag_field(tag_names),
            state.value,
            created_at.timestamp(),
            created_at.timestamp(),
            created_at.timestamp(),
        ),
    )

    return models.Todo(
        id=id,
        contents=contents,
        tags=tag_names,
        state=state,
        created_at=created_at,
        updated_at=created_at,
        state_updated_at=created_at,
    )


def update_todo(
    conn: sqlite3.Connection, todo_update: models.TodoUpdate
) -> models.Todo:
    todo = get_todo(conn, todo_update.id)
    if todo is None:
        raise DBException(f"todo with id '{todo_update.id}' does not exist")

    updated_at = datetime.now()
    if todo_update.state != todo.state:
        state_updated_at = updated_at
    else:
        state_updated_at = todo.state_updated_at

    conn.execute(
        """
        update todo set
        contents=?, tags=?, state=?, updated_at=?, state_updated_at=?
        where uuid=?
        """,
        (
            todo_update.contents,
            _get_tag_field(todo_update.tags),
            todo_update.state.value,
            updated_at.timestamp(),
            state_updated_at.timestamp(),
            todo_update.id,
        ),
    )

    todo.contents = todo_update.contents
    todo.tags = todo_update.tags
    todo.state = todo_update.state
    todo.updated_at = updated_at
    todo.state_updated_at = state_updated_at
    return todo


def _row_to_todo(row: Any) -> Optional[models.Todo]:
    if row is None:
        return None
    return models.Todo(
        id=row[0],
        contents=row[1],
        tags=_get_tag_names(row[2]),
        state=models.TodoState(row[3]),
        created_at=datetime.fromtimestamp(row[4]),
        updated_at=datetime.fromtimestamp(row[5]),
        state_updated_at=datetime.fromtimestamp(row[6]),
    )


def get_todo(conn: sqlite3.Connection, id: str) -> Optional[models.Todo]:
    cur = conn.execute(f"select {_ROWS} from todo where uuid=?", (id,))
    row = cur.fetchone()
    return _row_to_todo(row)


def get_all_todos(conn: sqlite3.Connection) -> List[models.Todo]:
    cur = conn.execute(f"select {_ROWS} from todo")
    rows = cur.fetchall()
    todos = [_row_to_todo(row) for row in rows]
    return cast(List[models.Todo], todos)


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
