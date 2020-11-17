from functools import lru_cache

from pydantic import BaseSettings


class Config(BaseSettings):
    db_path: str
    frontend_path: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_config() -> Config:
    return Config()
