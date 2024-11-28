#app/tests/api/users/test_users_endpoints.py
from faker import Faker
from fastapi.testclient import TestClient

from app.middleware.preset import settings

faker = Faker()


def test_get_public_user(
    client: TestClient, users_token_header: dict[str, str]
)-> None:
    req = client.get(f"{settings.API_V1_STR}/users/user", headers=users_token_header)
    current_user = req.json()
    assert current_user

