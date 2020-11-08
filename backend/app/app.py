from fastapi import FastAPI
from app.routes import todo, tag


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(tag.router, prefix="/api/tags")
    return app
