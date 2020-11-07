from typing import Any

import pytest

from app import config
from app.config import Config


@pytest.fixture(autouse=True)
def patch_config(monkeypath: Any) -> None:
    def patched_get_config() -> config.Config:
        return Config(db_path=":memory:")

    monkeypath.setattr(config, "get_config", patched_get_config)
