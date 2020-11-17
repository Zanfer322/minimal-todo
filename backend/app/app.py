from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import tag, todo
from app.config import get_config


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(tag.router, prefix="/api/tags")
    app.include_router(todo.router, prefix="/api/todo")
    config = get_config()
    app.mount("/todo", StaticFiles(directory=config.frontend_path, html=True))
    return app
