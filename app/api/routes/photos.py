#app/api/routes/photos.py

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import desc, func, select

from app import crud
from app.api.user_controllers import CurrentUser, SessionDep
from app.models import (
    Album,
    Message,
    Photo,
    PhotoCreate,
    PhotoPublic,
    PhotosPublic,
    PhotoUpdate,
)

router = APIRouter()

@router.post(
    "/",
    response_model=PhotoPublic
)
def create_photo(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    album_id: uuid.UUID,
    photo_in: PhotoCreate
) -> Any:
    """
    Create a new photo.
    """

    album = session.get(Album, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")


    photo = crud.get_photo_by_photo_title(db=session, photo_title=photo_in.photo_title, album_id=album_id)
    if photo:
        raise HTTPException(
            status_code=400, detail="A photo with this title already exists in this album"
        )
    new_photo = Photo(
        photo_title=photo_in.photo_title,
        image_url=photo_in.image_url,
        owner_id=current_user.id,
        album_id=album_id,
    )

    try:
        session.add(new_photo)
        session.commit()
        session.refresh(new_photo)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating photo: {str(e)}")

    return new_photo

@router.get("/{id}", response_model=PhotoPublic)
def get_photo(
    *,session:SessionDep, id:uuid.UUID
) -> Any:
    """
    Get photo by ID.
    """

    photo = session.get(Photo, id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo

@router.get("/", response_model=PhotosPublic)
def get_all_photos_in_an_album(
    *,session:SessionDep,current_user: CurrentUser, album_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get all photos for an album.
    """

    if current_user.is_superuser:
        statement = (
            select(Photo)
            .where(Photo.album_id == album_id)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Photo.updated_at))
        )
        photos = session.exec(statement).all()
        count_statement = select(func.count()).select_from(Photo)
        count = session.exec(count_statement).one()

    else:
        count_statement = (
            select(func.count())
            .select_from(Photo)
            .where(Photo.owner_id == current_user.id and Photo.album_id == album_id)

        )
        count = session.exec(count_statement).one()
        statement = (
            select(Photo)
            .where(Photo.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Photo.updated_at))
        )
        photos = session.exec(statement).all()

    return PhotosPublic(data=photos, count=count)

@router.put(
    "/{id}", response_model=PhotoPublic
)
def update_photo(
    *,session:SessionDep, current_user:CurrentUser, id:uuid.UUID, photo_in: PhotoUpdate
) -> Any:
    """
    Update an existing photo
    """

    photo =  session.get(Photo, id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    if photo_in.photo_title:
        existing_photo = crud.get_photo_by_photo_title(db=session, photo_title=photo_in.photo_title, album_id=photo.id)
        if existing_photo and existing_photo.id != photo.id:
            raise HTTPException(
                status_code=409, detail="Photo with this title already exist"
            )
    if not current_user.is_superuser and (photo.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    new_photo = crud.update_photo(db=session, photo=photo, photo_in=photo_in)

    return new_photo

@router.delete("/{id}")
def delete_photo(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an album
    """
    photo =  session.get(Photo, id)
    if not photo:
        raise HTTPException(status_code=404, detail="ALbum not found")
    if not current_user.is_superuser and (photo.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    session.delete(photo)
    session.commit()
    return Message(message="Photo deleted successfully")
