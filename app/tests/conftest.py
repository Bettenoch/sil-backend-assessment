from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.main import app
from app.middleware.db import engine, init_db
from app.models import User


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        # Initialize the database
        init_db(session)
        yield session

        # Clear the User table after tests
        statement = delete(User)
        session.execute(statement)  # Use `execute` for general SQL statements
        session.commit()
