import sqlite3
from functools import lru_cache

from app import config


@lru_cache
def get_connection() -> sqlite3.Connection:
    cfg = config.get_config()
    conn = sqlite3.connect(cfg.db_path, check_same_thread=False)
    return conn
