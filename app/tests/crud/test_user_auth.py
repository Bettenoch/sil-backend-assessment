from faker import Faker
from sqlmodel import Session

from app import crud
from app.models import UserCreate

faker = Faker()

sample_email = faker.email()
sample_username = faker.user_name()
sample_fullname = faker.name()
sample_avatar = faker.image_url()
sample_password = faker.password()


def test_create_user(db: Session) -> None:
    name = sample_fullname
    username = sample_username
    email = sample_email
    password = sample_password

    user_in = UserCreate(email=email, password=password, name=name, username=username)
    user = crud.create_user(db=db, create_user=user_in)

    assert user.username == username
    assert user.name == name
    assert user.email == email
    assert hasattr(user, "hashed_password")
