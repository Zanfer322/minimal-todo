import sqlite3
from functools import lru_cache
from pathlib import Path

from app import config


@lru_cache
def get_connection() -> sqlite3.Connection:
    cfg = config.get_config()
    conn = sqlite3.connect(cfg.db_path, check_same_thread=False)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    init_sql_path = Path(__file__).parent / 'init.sql'

    with open(init_sql_path) as file:
        init_sql = file.read()

    conn.executescript(init_sql)
