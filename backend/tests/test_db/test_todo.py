import pytest
import sqlite3
import time
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
    pass


def test_get_unknown_todo(conn: sqlite3.Connection) -> None:
    pass
