from datetime import datetime
from typing import List, Optional, Set

from fastapi import APIRouter, HTTPException, status

from app import db, models

router = APIRouter()


@router.post("/", response_model=models.Todo)
def create_todo(create_todo: models.CreateTodo) -> models.Todo:
    conn = db.get_connection()
    todo = db.create_todo(conn, create_todo.contents, create_todo.tags)
    return todo


@router.get("/", response_model=List[models.Todo])
def get_todos(
    state: Optional[models.TodoState] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    tags: Optional[Set[str]] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[models.Todo]:
    conn = db.get_connection()
    todos = db.get_filtered_todos(
        conn, state, start_time, end_time, tags, limit, offset
    )
    return todos


@router.put("/", response_model=models.Todo)
def update_todo(todo_update: models.TodoUpdate) -> models.Todo:
    conn = db.get_connection()
    try:
        todo = db.update_todo(conn, todo_update)
    except db.DBException as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    return todo


@router.get("/search", response_model=List[models.Todo])
def search_term(
    search_term: str, limit: Optional[int] = None, offset: Optional[int] = None
) -> List[models.Todo]:
    conn = db.get_connection()
    todos = db.search_todo(conn, search_term, limit, offset)
    return todos


@router.get("/{id}", response_model=models.Todo)
def get_todo(id: str) -> models.Todo:
    conn = db.get_connection()
    todo = db.get_todo(conn, id)
    if todo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return todo
