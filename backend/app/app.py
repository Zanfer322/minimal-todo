from fastapi import FastAPI

from app.routes import tag, todo


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(tag.router, prefix="/api/tags")
    app.include_router(todo.router, prefix="/api/todo")
    return app
