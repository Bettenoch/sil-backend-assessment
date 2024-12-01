# app/crud.py

import uuid
from typing import Any

from sqlmodel import Session, and_, select

from app.middleware.user_auth import get_hashed_password, verify_password
from app.models import (
    Album,
    AlbumCreate,
    AlbumUpdate,
    Photo,
    PhotoCreate,
    PhotoUpdate,
    User,
    UserCreate,
    UserUpdate,
)


def create_user(*, create_user: UserCreate, db: Session) -> User:
    hashed_password = get_hashed_password(create_user.password)

    user_obj = User.model_validate(
        create_user, update={"hashed_password": hashed_password}
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


def update_user(*, db: Session, inst_user: User, user_in: UserUpdate) -> Any:
    user_obj = user_in.model_dump(exclude_unset=True)
    auth_data = {}
    if "password" in user_obj:
        password = user_obj["password"]
        hash_password = get_hashed_password(password)
        auth_data["hashed_password"] = hash_password

    inst_user.sqlmodel_update(user_obj, update=auth_data)
    db.add(inst_user)
    db.commit()
    db.refresh(inst_user)
    return inst_user


def get_user_by_username(*, db: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    inst_user = db.exec(statement).first()
    return inst_user


def authenticate_by_username_and_email(
    *, db: Session, username: str, email: str
) -> User | None:
    statement = select(User).where(and_(User.username == username, User.email == email))
    inst_user = db.exec(statement).first()
    if not inst_user:
        return None
    return inst_user


def get_user_by_email(*, db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    inst_user = db.exec(statement).first()
    return inst_user


def authenticate_by_password(*, db: Session, email: str, password: str) -> User | None:
    inst_user = get_user_by_email(db=db, email=email)
    if not inst_user:
        return None
    if not verify_password(password, inst_user.hashed_password):
        return None
    return inst_user


# ----------ALBUMS CRUDS OPERATIONS--------


def create_album(
    *, db: Session, create_album: AlbumCreate, owner_id: uuid.UUID
) -> Album:
    album = Album.model_validate(create_album, update={"owner_id": owner_id})
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


def update_album(*, db: Session, album: Album, album_in: AlbumUpdate) -> Album:
    album_obj = album_in.model_dump(exclude_unset=True)
    album.sqlmodel_update(album_obj)
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


def get_album_bg_id(
    *,
    db: Session,
    album_id: uuid.UUID,
) -> Album | None:
    query = select(Album).where(Album.id == album_id)
    album = db.exec(query).first()
    return album

def get_album_by_title(
    *,
    db: Session,
    title: str
)-> Album | None:
    statement = select(Album).where(Album.title == title)
    inst_album = db.exec(statement).first()
    return inst_album


# ----------PHOTOS CURDS OPERATIONS--------


def create_photo(
    *, db: Session, create_photo: PhotoCreate, owner_id: uuid.UUID
) -> Photo:
    photo = Photo.model_validate(
        create_photo,
        update={
            "owner_id": owner_id,
            "album_id": create_photo.album_id,
        },
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


def update_photo(*, db: Session, photo: Photo, photo_in: PhotoUpdate) -> Photo:
    photo_obj = photo_in.model_dump(exclude_unset=True)
    photo.sqlmodel_update(photo_obj)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

