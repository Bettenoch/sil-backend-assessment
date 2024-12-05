# app/api/routes/get_album_photos.py

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import desc, func, select

from app.api.user_controllers import SessionDep
from app.crud import get_album_owner_id
from app.models import (
    Photo,
    PhotoPublic,
    PhotosPublic,
    User,
)

router = APIRouter()


@router.get("/", response_model=PhotosPublic)
def get_all_album_photos(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    album_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all photos for an album.
    """

    album_owner_id = get_album_owner_id(db=session, album_id=album_id)
    if album_owner_id != user_id:
        raise HTTPException(status_code=403, detail="This user does not own this album")
    statement = (
        select(Photo)
        .where(Photo.album_id == album_id)
        .offset(skip)
        .limit(limit)
        .order_by(desc(Photo.updated_at))
    )
    photos = session.exec(statement).all()
    count_statement = (
        select(func.count()).select_from(Photo).where(Photo.album_id == album_id)
    )
    count = session.exec(count_statement).one()

    return PhotosPublic(data=photos, count=count)


@router.get("/{id}", response_model=PhotoPublic)
def get_photo_id(
    *, session: SessionDep, user_id: uuid.UUID, album_id: uuid.UUID, id: uuid.UUID
) -> Any:
    """
    Get photo by ID.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    album_owner_id = get_album_owner_id(db=session, album_id=album_id)
    if album_owner_id != user_id:
        raise HTTPException(status_code=403, detail="This user does not own this album")
    photo = session.get(Photo, id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo
