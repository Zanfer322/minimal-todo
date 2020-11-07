import sqlite3
from app import db
from tests import helpers
import pytest


def test_create_tag(conn: sqlite3.Connection) -> None:
    tag = db.create_tag(conn, "tag name")
    db_tag = db.get_tag(conn, tag.id)

    assert tag == db_tag
    assert tag.name == "tag name"
    assert helpers.is_recent(tag.created_at)


def test_create_multiple_tags(conn: sqlite3.Connection) -> None:
    tag = db.create_tag(conn, "tag name")
    tag_2 = db.create_tag(conn, "tag name 2")

    db_tag = db.get_tag(conn, tag.id)
    db_tag_2 = db.get_tag(conn, tag_2.id)

    assert tag == db_tag
    assert tag_2 == db_tag_2

    db_tags = db.get_all_tags(conn)
    assert len(db_tags) == 2


def test_duplicate_tags(conn: sqlite3.Connection) -> None:
    db.create_tag(conn, "tag")

    with pytest.raises(db.DBException):
        db.create_tag(conn, "tag")


def test_get_unknown_tag(conn: sqlite3.Connection) -> None:
    tag = db.get_tag(conn, "unknown-id")
    assert tag is None
