import sqlite3
from datetime import datetime
import uuid
from typing import List, Optional
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
    if row is None:
        return None

    return models.Tag(id=row[0], name=row[1], created_at=datetime.fromtimestamp(row[2]))


def get_all_tags(conn: sqlite3.Connection) -> List[models.Tag]:
    cur = conn.execute("select uuid, tag, created_at from tags")
    rows = cur.fetchall()

    return [models.Tag(id=row[0], name=row[1], created_at=row[2]) for row in rows]
