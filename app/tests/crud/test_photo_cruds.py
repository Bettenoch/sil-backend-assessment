# app/tests/crud/test_photo_cruds.py
from faker import Faker
from fastapi import HTTPException
from sqlmodel import Session

from app import crud
from app.models import AlbumCreate, Photo, PhotoCreate, UserCreate

faker = Faker()

sample_email = faker.email()
sample_username = faker.user_name()
sample_fullname = faker.name()
sample_avatar = faker.image_url()
sample_password = faker.password()


def test_photo_create(*, db: Session) -> None:
    name = sample_fullname
    username = sample_username
    email = sample_email
    password = sample_password

    user_in = UserCreate(email=email, password=password, name=name, username=username)
    user = crud.create_user(db=db, create_user=user_in)
    user_id = user.id
    title = faker.name()
    description = "First test book"

    album_in = AlbumCreate(title=title, description=description)
    album = crud.create_album(db=db, create_album=album_in, owner_id=user_id)

    album_id = album.id
    photo_title = faker.file_name()
    image_url = faker.image_url()

    photo = Photo(
        photo_title=photo_title,
        image_url=image_url,
        owner_id=user_id,
        album_id=album_id,
    )
    

    db.add(photo)
    db.commit()
    db.refresh(photo)


    assert photo.photo_title == photo_title
    assert photo.image_url == image_url
    assert photo.owner_id == album.owner_id
