import sqlite3
import time
from datetime import datetime

import pytest

from app import db, models
from tests import helpers


def test_create_todo(conn: sqlite3.Connection) -> None:
    db.create_tag(conn, "a")
    db.create_tag(conn, "b")

    todo = db.create_todo(conn, "contents", {"a", "b"})
    db_todo = db.get_todo(conn, todo.id)

    assert todo == db_todo
    assert todo.contents == "contents"
    assert todo.tags == {"a", "b"}
    assert helpers.is_recent(todo.created_at)
    assert todo.created_at == todo.updated_at
    assert todo.created_at == todo.state_updated_at


def test_create_todo_with_invalid_tags(conn: sqlite3.Connection) -> None:
    db.create_tag(conn, "a")

    with pytest.raises(db.DBException):
        db.create_todo(conn, "contents", {"a", "b"})


def test_create_multiple_todos(conn: sqlite3.Connection) -> None:
    db.create_tag(conn, "a")

    todo = db.create_todo(conn, "contents", {"a"})
    todo_2 = db.create_todo(conn, "contents 2", set())

    db_todos = db.get_all_todos(conn)

    assert len(db_todos) == 2

    left = {todo.id: todo, todo_2.id: todo_2}
    right = {t.id: t for t in db_todos}

    assert left == right


def test_update_todo_without_state_change(conn: sqlite3.Connection) -> None:
    db.create_tag(conn, "a")
    todo = db.create_todo(conn, "contents", set())
    todo_update = models.TodoUpdate(
        id=todo.id, contents="new contents", tags={"a"}, state=todo.state
    )

    time.sleep(0.1)
    new_todo = db.update_todo(conn, todo_update)
    db_todo = db.get_todo(conn, todo.id)

    assert new_todo == db_todo
    assert db_todo.contents == "new contents"
    assert db_todo.tags == {"a"}
    assert db_todo.updated_at > db_todo.created_at
    assert db_todo.state_updated_at == db_todo.created_at


def test_update_todo_with_state_change(conn: sqlite3.Connection) -> None:
    db.create_tag(conn, "a")
    todo = db.create_todo(conn, "contents", set())
    todo_update = models.TodoUpdate(
        id=todo.id, contents="new contents", tags={"a"}, state=models.TodoState.done
    )

    time.sleep(0.1)
    new_todo = db.update_todo(conn, todo_update)
    db_todo = db.get_todo(conn, todo.id)

    assert new_todo == db_todo
    assert db_todo.contents == "new contents"
    assert db_todo.tags == {"a"}
    assert db_todo.updated_at > db_todo.created_at
    assert db_todo.state_updated_at == db_todo.updated_at


def test_update_unknown_todo(conn: sqlite3.Connection) -> None:
    todo_update = models.TodoUpdate(
        id="unknown-id", contents="contents", tags=set(), state=models.TodoState.ongoing
    )
    with pytest.raises(db.DBException):
        db.update_todo(conn, todo_update)


def test_get_unknown_todo(conn: sqlite3.Connection) -> None:
    todo = db.get_todo(conn, "unknown-id")
    assert todo is None

    todos = db.get_all_todos(conn)
    assert len(todos) == 0


def _create_dummy_data(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT INTO tags (id, uuid, tag, created_at) VALUES (?, ?, ?, ?)",
        [
            (1, "1", "t1", 100_000),
            (2, "2", "t2", 100_000),
            (3, "3", "t3", 100_000),
        ],
    )

    conn.executemany(
        """
        INSERT INTO todo
        (uuid, contents, tags, state, created_at, updated_at, state_updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            ("1", "c1", "3 2 1", "ongoing", 110_000, 110_00, 110_000),
            ("2", "c2", "2", "done", 120_000, 120_000, 120_000),
            ("3", "c3", "3", "cancelled", 130_000, 130_000, 130_000),
            ("4", "c4", "1", "cancelled", 210_000, 210_000, 210_000),
            ("5", "c5", "2", "ongoing", 220_000, 220_000, 220_000),
            ("6", "c6", "3", "done", 230_000, 230_000, 230_000),
        ],
    )


def test_can_filter_by_state(conn: sqlite3.Connection) -> None:
    _create_dummy_data(conn)
    todos = db.get_filtered_todos(conn, state=models.TodoState.done)

    assert set([t.id for t in todos]) == {"2", "6"}


def test_can_filter_by_start_time(conn: sqlite3.Connection) -> None:
    _create_dummy_data(conn)
    todos = db.get_filtered_todos(conn, start_time=datetime.fromtimestamp(200_000))

    assert set([t.id for t in todos]) == {"4", "5", "6"}


def test_can_filter_by_end_time(conn: sqlite3.Connection) -> None:
    _create_dummy_data(conn)
    todos = db.get_filtered_todos(conn, end_time=datetime.fromtimestamp(200_000))

    assert set([t.id for t in todos]) == {"1", "2", "3"}


def test_can_filter_by_both_time(conn: sqlite3.Connection) -> None:
    _create_dummy_data(conn)
    todos = db.get_filtered_todos(
        conn,
        start_time=datetime.fromtimestamp(115_000),
        end_time=datetime.fromtimestamp(200_000),
    )

    assert set([t.id for t in todos]) == {"2", "3"}


def test_can_filter_by_tag(conn: sqlite3.Connection) -> None:
    _create_dummy_data(conn)
    todos = db.get_filtered_todos(conn, tag_names={"t1"})
    assert set([t.id for t in todos]) == {"1", "4"}

    todos = db.get_filtered_todos(conn, tag_names={"t2", "t1"})
    assert set([t.id for t in todos]) == {"1"}


def test_full_text_search(conn: sqlite3.Connection) -> None:
    db.create_todo(conn, "normal content", set())
    db.create_todo(conn, "special content", set())
    db.create_todo(conn, "very content special", set())

    todos = db.search_todo(conn, "content", limit=2)
    assert len(todos) == 2
    assert set([t.contents for t in todos]) == {"normal content", "special content"}

    todos = db.search_todo(conn, "very special")
    assert len(todos) == 1
    assert todos[0].contents == "very content special"
