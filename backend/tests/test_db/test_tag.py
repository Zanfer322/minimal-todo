import sqlite3

import pytest

from app import db
from tests import helpers


def test_create_tag(conn: sqlite3.Connection) -> None:
    tag = db.create_tag(conn, "tag name")
    db_tag = db.get_tag(conn, tag.id)

    assert tag == db_tag
    assert tag.name == "tag name"
    assert helpers.is_recent(tag.created_at)


def test_create_multiple_tags(conn: sqlite3.Connection) -> None:
    tag = db.create_tag(conn, "tag name")
    tag_2 = db.create_tag(conn, "tag name 2")

    db_tags = db.get_all_tags(conn)
    assert len(db_tags) == 2

    left = {tag.id: tag, tag_2.id: tag_2}
    right = {t.id: t for t in db_tags}

    assert left == right


def test_duplicate_tags(conn: sqlite3.Connection) -> None:
    db.create_tag(conn, "tag")

    with pytest.raises(db.DBException):
        db.create_tag(conn, "tag")


def test_get_tag_by_name(conn: sqlite3.Connection) -> None:
    tag = db.create_tag(conn, "tag")
    db_tag = db.get_tag_by_name(conn, "tag")

    assert tag == db_tag


def test_get_unknown_tag(conn: sqlite3.Connection) -> None:
    tag = db.get_tag(conn, "unknown-id")
    assert tag is None

    tag = db.get_tag_by_name(conn, "unknown name")
    assert tag is None
