from fastapi.testclient import TestClient

from app.middleware.preset import settings


def get_superuser_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    req = client.post(f"{settings.API_V1_STR}/login/authenticated_token", data=login_data)
    tokens = req.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
