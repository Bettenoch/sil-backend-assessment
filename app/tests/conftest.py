from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session, delete
from collections.abc import Generator
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
        init_db(session)
        yield session
        statement = delete(User)
        session.exec(statement)
        session.commit()
