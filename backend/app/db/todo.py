import sqlite3
import uuid
from datetime import datetime
from typing import Any, List, Optional, Set, Union, cast

from app import models

from .exceptions import DBException
from .tag import get_tag_by_db_id, get_tags_by_name

_ROWS = "uuid, contents, tags, state, created_at, updated_at, state_updated_at"


def _verify_tags(conn: sqlite3.Connection, tag_names: Set[str]) -> None:
    tags = get_tags_by_name(conn, tag_names)
    found_tag_names = set([t.name for t in tags if t is not None])

    if None in tags:
        raise DBException(f"invalid tags '{tag_names - found_tag_names}'")


def _get_tag_field(conn: sqlite3.Connection, tag_names: Set[str]) -> Optional[str]:
    if not len(tag_names):
        return None
    tags = get_tags_by_name(conn, tag_names)
    x = " ".join([str(t.db_id) for t in tags if t is not None])
    print(x)
    return x


def _get_tag_names(conn: sqlite3.Connection, tag_field: Optional[str]) -> Set[str]:
    if tag_field is None:
        return set()
    ids = [int(x) for x in tag_field.split(" ")]
    tags = [get_tag_by_db_id(conn, id) for id in ids]
    tag_names = [tag.name for tag in tags if tag is not None]
    return set(tag_names)


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
            _get_tag_field(conn, tag_names),
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

    _verify_tags(conn, todo_update.tags)
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
            _get_tag_field(conn, todo_update.tags),
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


def _row_to_todo(conn: sqlite3.Connection, row: Any) -> Optional[models.Todo]:
    if row is None:
        return None
    return models.Todo(
        id=row[0],
        contents=row[1],
        tags=_get_tag_names(conn, row[2]),
        state=models.TodoState(row[3]),
        created_at=datetime.fromtimestamp(row[4]),
        updated_at=datetime.fromtimestamp(row[5]),
        state_updated_at=datetime.fromtimestamp(row[6]),
    )


def get_todo(conn: sqlite3.Connection, id: str) -> Optional[models.Todo]:
    cur = conn.execute(f"select {_ROWS} from todo where uuid=?", (id,))
    row = cur.fetchone()
    return _row_to_todo(conn, row)


def get_all_todos(conn: sqlite3.Connection) -> List[models.Todo]:
    cur = conn.execute(f"select {_ROWS} from todo")
    rows = cur.fetchall()
    todos = [_row_to_todo(conn, row) for row in rows]
    return cast(List[models.Todo], todos)


def get_filtered_todos(
    conn: sqlite3.Connection,
    state: Optional[models.TodoState] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    tag_names: Optional[Set[str]] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[models.Todo]:
    query = f"select {_ROWS} from todo"

    filter_statements = []
    query_params = []

    if state is not None:
        filter_statements.append("state=?")
        query_params.append(state.value)

    if start_time is not None:
        filter_statements.append("created_at > ?")
        query_params.append(start_time.timestamp())

    if end_time is not None:
        filter_statements.append("created_at < ?")
        query_params.append(end_time.timestamp())

    if tag_names is not None and len(tag_names) != 0:
        filter_statements.append(
            "id in (SELECT rowid from fts_tag WHERE fts_tag MATCH ?)"
        )
        query_params.append(_get_tag_field(conn, tag_names))

    if len(filter_statements) != 0:
        query += " where "
        query += " and ".join(filter_statements)

    if offset is not None and limit is None:
        # Offset is not possible without limit. Limit = -1 is effectively no limit
        limit = -1

    if limit is not None:
        query += " limit ?"
        query_params.append(limit)

    if offset is not None:
        query += " offset ?"
        query_params.append(offset)

    # TODO: remove print statement
    print(query)
    cur = conn.execute(query, query_params)
    rows = cur.fetchall()
    todos = [_row_to_todo(conn, row) for row in rows]
    return cast(List[models.Todo], todos)


def search_todo(
    conn: sqlite3.Connection,
    search_term: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[models.Todo]:
    query = "SELECT rowid, rank from fts_todo WHERE fts_todo MATCH ? ORDER BY rank"

    query_params: List[Union[str, int]] = [search_term]

    if offset is not None and limit is None:
        # Offset is not possible without limit. Limit = -1 is effectively no limit
        limit = -1

    if limit is not None:
        query += " limit ?"
        query_params.append(limit)

    if offset is not None:
        query += " offset ?"
        query_params.append(offset)

    id_cur = conn.execute(query, query_params)
    id_rows = id_cur.fetchall()
    ids = [row[0] for row in id_rows]
    print(ids)

    todo_query = (
        f"select {_ROWS} from todo where id in ({','.join(['?' for _ in ids])})"
    )
    todo_cur = conn.execute(todo_query, ids)
    todo_rows = todo_cur.fetchall()
    todos = [_row_to_todo(conn, row) for row in todo_rows]
    return cast(List[models.Todo], todos)
