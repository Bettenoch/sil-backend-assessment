# app/tests/confest.py
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.middleware.db import engine, init_db
from app.middleware.preset import settings
from app.tests.utils.token_gen import get_superuser_headers
from app.tests.utils.user_auth import get_email_auth_token


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        # Initialize the database
        init_db(session)
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def users_token_header(client: TestClient, db: Session) -> dict[str, str]:
    return get_email_auth_token(
        client=client, session=db, email=settings.EMAIL_TEST_USER
    )


@pytest.fixture(scope="module")
def superuser_token(client: TestClient) -> dict[str, str]:
    return get_superuser_headers(client)
