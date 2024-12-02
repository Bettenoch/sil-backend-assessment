# app/api/routes/albums.py

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import desc, func, select

from app import crud
from app.api.user_controllers import CurrentUser, SessionDep
from app.models import (
    Album,
    AlbumCreate,
    AlbumPublic,
    AlbumsPublic,
    AlbumUpdate,
    Message,
)

router = APIRouter()


@router.get("/", response_model=AlbumsPublic)
def get_albums(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    GET ALL ALBUMS
    """

    total_statement = select(func.count()).select_from(Album)
    count = session.exec(total_statement).one()

    statement = select(Album).offset(skip).limit(limit).order_by(desc(Album.updated_at))
    albums = session.exec(statement).all()

    return AlbumsPublic(data=albums, count=count)


@router.get("/{id}", response_model=AlbumPublic)
def get_album(session: SessionDep, id: uuid.UUID) -> Any:
    """
    GET ALL ALBUMS
    """

    album = session.get(Album, id)

    if not album:
        raise HTTPException(status_code=404, detail="Item not found")
    return album


@router.post("/", response_model=AlbumPublic)
def create_album(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    album_in: AlbumCreate,
) -> Any:
    """
    CREATE AN ALBUM
    """
    album = crud.get_album_by_title(db=session, title=album_in.title)

    if album:
        raise HTTPException(
            status_code=400, detail="An album with this title already exists"
        )
    album = crud.create_album(
        db=session, create_album=album_in, owner_id=current_user.id
    )
    return album


@router.put("/{id}", response_model=AlbumPublic)
def update_album(
    *,
    session: SessionDep,
    id: uuid.UUID,
    album_in: AlbumUpdate,
    current_user: CurrentUser,
) -> Any:
    """
    UPDATE AN ALBUM
    """
    album = session.get(Album, id)
    if not album:
        raise HTTPException(status_code=404, detail="ALbum not found")

    if album_in.title:
        existing_album = crud.get_album_by_title(db=session, title=album_in.title)
        if existing_album and existing_album.id != album.id:
            raise HTTPException(
                status_code=409, detail="Album with this title already exist"
            )
    if not current_user.is_superuser and (album.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    new_album = crud.update_album(db=session, album=album, album_in=album_in)
    return new_album


@router.delete("/{id}")
def delete_album(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an album
    """
    album = session.get(Album, id)
    if not album:
        raise HTTPException(status_code=404, detail="ALbum not found")
    if not current_user.is_superuser and (album.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    session.delete(album)
    session.commit()
    return Message(message="Album deleted successfully")
