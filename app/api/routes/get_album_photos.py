# app/api/routes/get_album_photos.py

import uuid
from typing import Any

from fastapi import APIRouter
from sqlmodel import desc, func, select

from app.api.user_controllers import SessionDep
from app.models import (
    Photo,
    PhotosPublic,
)

router = APIRouter()


@router.get("/", response_model=PhotosPublic)
def get_all_photos_in_an_album(
    *,
    session: SessionDep,
    album_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all photos for an album.
    """

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
