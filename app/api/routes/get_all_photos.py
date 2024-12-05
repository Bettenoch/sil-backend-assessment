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
def get_all_photos(
    *,
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all photos for an album.
    """

    statement = select(Photo).offset(skip).limit(limit).order_by(desc(Photo.updated_at))
    photos = session.exec(statement).all()
    count_statement = select(func.count()).select_from(Photo)
    count = session.exec(count_statement).one()

    return PhotosPublic(data=photos, count=count)
