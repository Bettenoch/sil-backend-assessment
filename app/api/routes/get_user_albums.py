import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import desc, func, select

from app.api.user_controllers import SessionDep
from app.models import (
    Album,
    AlbumPublic,
    AlbumsPublic,
    User,
)

router = APIRouter()


@router.get("/", response_model=AlbumsPublic)
def get_all_user_albums(
    session: SessionDep, user_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> Any:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_statement = (
        select(func.count()).select_from(Album).where(Album.owner_id == user.id)
    )
    count = session.exec(total_statement).one()

    statement = (
        select(Album)
        .where(Album.owner_id == user.id)
        .offset(skip)
        .limit(limit)
        .order_by(desc(Album.updated_at))
    )
    albums = session.exec(statement).all()
    return AlbumsPublic(data=albums, count=count)


@router.get("/{id}", response_model=AlbumPublic)
def get_album_id(session: SessionDep, user_id: uuid.UUID, id: uuid.UUID) -> Any:
    """
    GET ALL ALBUMS
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    album = session.get(Album, id)

    if not album:
        raise HTTPException(status_code=404, detail="Item not found")
    return album
