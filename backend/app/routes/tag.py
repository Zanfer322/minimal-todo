from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from app import db, models

router = APIRouter()


@router.get("/", response_model=List[models.APITag])
def get_all_tags(name: Optional[str] = None) -> List[models.Tag]:
    conn = db.get_connection()
    tags = db.get_all_tags(conn)
    return tags


@router.get("/name", response_model=models.APITag)
def get_tag_by_name(name: str) -> models.Tag:
    conn = db.get_connection()
    tag = db.get_tag_by_name(conn, name)
    if tag is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return tag


@router.get("/{id}", response_model=models.APITag)
def get_tag(id: str) -> models.Tag:
    conn = db.get_connection()
    tag = db.get_tag(conn, id)
    if tag is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return tag


@router.post("/", response_model=models.APITag)
def create_tag(create_tag: models.CreateTag) -> models.Tag:
    conn = db.get_connection()
    try:
        tag = db.create_tag(conn, create_tag.name)
    except db.DBException as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    return tag
