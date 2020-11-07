import sqlite3
from typing import Any

import pytest

from app import config
from app.config import Config
from app import db


@pytest.fixture(autouse=True)
def patch_config(monkeypatch: Any) -> None:
    def patched_get_config() -> config.Config:
        return Config(db_path=":memory:")

    monkeypatch.setattr(config, "get_config", patched_get_config)


@pytest.fixture
def conn() -> sqlite3.Connection:
    conn = sqlite3.connect(':memory:')
    db.init_db(conn)
    return conn
