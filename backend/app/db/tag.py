import sqlite3
from datetime import datetime
import uuid
from typing import Any, List, Optional, cast, Set
from app import models
from .exceptions import DBException


def create_tag(conn: sqlite3.Connection, name: str) -> models.Tag:
    id = uuid.uuid4().hex
    created_at = datetime.now()

    try:
        conn.execute(
            "insert into tags(uuid, tag, created_at) values (?, ?, ?)",
            (id, name, created_at.timestamp()),
        )
    except sqlite3.IntegrityError as e:
        msg = str(e)
        if "UNIQUE" in msg and "tags.tag" in msg:
            raise DBException(f"tag with name '{name}' already exists")
        raise

    tag = models.Tag(id=id, name=name, created_at=created_at)
    return tag


def get_tag(conn: sqlite3.Connection, id: str) -> Optional[models.Tag]:
    cur = conn.execute("select uuid, tag, created_at from tags where uuid=?", (id,))
    row = cur.fetchone()
    return _row_to_tag(row)


def get_tag_by_name(conn: sqlite3.Connection, name: str) -> Optional[models.Tag]:
    cur = conn.execute("select uuid, tag, created_at from tags where tag=?", (name,))
    row = cur.fetchone()
    return _row_to_tag(row)


def get_all_tags(conn: sqlite3.Connection) -> List[models.Tag]:
    cur = conn.execute("select uuid, tag, created_at from tags")
    rows = cur.fetchall()
    tags = [_row_to_tag(row) for row in rows]
    return cast(List[models.Tag], tags)


def get_tags_by_name(
    conn: sqlite3.Connection, names: Set[str]
) -> List[Optional[models.Tag]]:
    # TODO: optimize
    return [get_tag_by_name(conn, name) for name in names]


def _row_to_tag(row: Optional[Any]) -> Optional[models.Tag]:
    if row is None:
        return row

    return models.Tag(id=row[0], name=row[1], created_at=datetime.fromtimestamp(row[2]))
