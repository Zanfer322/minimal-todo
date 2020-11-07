import sqlite3
from typing import List
from app import models


def create_tag(conn: sqlite3.Connection, name: str) -> models.Tag:
    pass


def get_tag(conn: sqlite3.Connection, id: str) -> models.Tag:
    pass


def get_all_tags(conn: sqlite3.Connection) -> List[models.Tag]:
    pass
