import sqlite3
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app import config, app, db
from app.config import Config


@pytest.fixture(autouse=True)
def patch_config(monkeypatch: Any) -> None:
    def patched_get_config() -> config.Config:
        return Config(db_path=":memory:")

    monkeypatch.setattr(config, "get_config", patched_get_config)


@pytest.fixture
def conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    db.init_db(conn)
    return conn


@pytest.fixture
def client() -> TestClient:
    db.get_connection.cache_clear()
    conn = db.get_connection()
    db.init_db(conn)
    return TestClient(app)
