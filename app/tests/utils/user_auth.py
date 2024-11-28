# app/tests/utils/user_auth.py

from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.middleware.preset import settings
from app.models import User, UserCreate, UserUpdate

faker = Faker()


def create_test_user(session: Session) -> User:
    sample_email = faker.email()
    sample_username = faker.user_name()
    sample_fullname = faker.name()
    sample_password = faker.password()

    user_in = UserCreate(
        email=sample_email,
        username=sample_username,
        name=sample_fullname,
        password=sample_password,
    )
    user = crud.create_user(db=session, create_user=user_in)
    return user


def user_auth_headers(
    *, client: TestClient, email: str, password: str
) -> dict[str, str]:
    user_obj = {"username": email, "password": password}

    req = client.post(f"{settings.API_V1_STR}/login/authenticated_token", data=user_obj)
    res = req.json()
    token = res["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def get_email_auth_token(
    *, client: TestClient, email: str, session: Session
) -> dict[str, str]:
    password = faker.password()
    name = faker.name()
    username = faker.user_name()
    user = crud.get_user_by_email(db=session, email=email)
    if not user:
        user_in = UserCreate(
            email=email, name=name, username=username, password=password
        )
        user = crud.create_user(db=session, create_user=user_in)

    else:
        user_in_update = UserUpdate(password=password)
        if not user.id:
            raise Exception("User id not set")
        user = crud.update_user(db=session, inst_user=user, user_in=user_in_update)
    return user_auth_headers(client=client, email=email, password=password)
