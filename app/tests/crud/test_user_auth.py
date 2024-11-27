from faker import Faker
from sqlmodel import Session

from app import crud
from app.middleware.user_auth import verify_password
from app.models import User, UserCreate, UserUpdate

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


def test_user_authenticate(db: Session) -> None:
    name = faker.name()
    username = faker.user_name()
    email = faker.email()
    password = faker.password()

    user_in = UserCreate(email=email, name=name, username=username, password=password)

    user = crud.create_user(db=db, create_user=user_in)

    authenticated_user = crud.authenticate_by_password(
        db=db, email=email, password=password
    )
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_should_authenticate_with_username(db: Session) -> None:
    name = faker.name()
    username = faker.user_name()
    email = faker.email()
    password = faker.password()

    user_in = UserCreate(email=email, name=name, username=username, password=password)

    user = crud.create_user(db=db, create_user=user_in)
    authenticated_user = crud.authenticate_by_username_and_email(
        db=db, email=email, username=username
    )
    assert authenticated_user
    assert user.username == authenticated_user.username
    assert user.is_superuser is False


def test_check_user_is_superuser(db: Session) -> None:
    name = faker.name()
    username = faker.user_name()
    email = faker.email()
    password = faker.password()

    user_in = UserCreate(
        email=email, name=name, username=username, password=password, is_superuser=True
    )

    user = crud.create_user(db=db, create_user=user_in)
    assert user.is_superuser is True


def test_should_update_user(db: Session) -> None:
    name = faker.name()
    username = faker.user_name()
    email = faker.email()
    password = faker.password()
    user_in = UserCreate(
        email=email, name=name, username=username, password=password, is_superuser=True
    )
    user = crud.create_user(db=db, create_user=user_in)
    new_password = faker.password()
    user_update = UserUpdate(password=new_password, is_superuser=True)
    if user.id is not None:
        crud.update_user(db=db, inst_user=user, user_in=user_update)

    updated_user = db.get(User, user.id)
    assert updated_user
    assert user.email == updated_user.email
    assert verify_password(new_password, updated_user.hashed_password)
