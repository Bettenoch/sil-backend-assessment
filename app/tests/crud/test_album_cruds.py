# app/tests/crud/test_album_cruds.py

from faker import Faker
from sqlmodel import Session

from app import crud
from app.models import AlbumCreate, UserCreate

faker = Faker()

sample_email = faker.email()
sample_username = faker.user_name()
sample_fullname = faker.name()
sample_avatar = faker.image_url()
sample_password = faker.password()


def test_album_create(db: Session) -> None:
    # user create
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

    assert album.title == title
