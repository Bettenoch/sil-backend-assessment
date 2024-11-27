from fastapi.testclient import TestClient
from app.middleware.preset import settings


def test_get_user_access_token(client:TestClient):
    user_obj = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    
    req = client.post(f"{settings.API_V1_STR}/login/authenticated_token",data=user_obj)
    token = req.json()
    assert req.status_code == 200
    assert "access_token" in token
    assert token["access_token"]
    