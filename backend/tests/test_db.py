import sqlite3
from app import db
from . import helpers


def test_create_tag(conn: sqlite3.Connection) -> None:
    tag = db.create_tag(conn, "tag name")
    db_tag = db.get_tag(conn, tag.id)

    assert tag == db_tag
    assert tag.name == "tag name"
    assert helpers.is_recent(tag.created_at)
