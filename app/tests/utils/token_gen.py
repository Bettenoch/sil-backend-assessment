# from app.middleware.preset import settings

# from fastapi.testclient import TestClient

# def get_superuser_headers(client: TestClient) -> dict[str, str]:
#     login_data = {
#         "username": settings.FIRST_SUPERUSER_NAME,
#         "password": settings.FIRST_SUPERUSER_PASSWORD,
#     }
#     r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
#     tokens = r.json()
#     a_token = tokens["access_token"]
#     headers = {"Authorization": f"Bearer {a_token}"}
#     return headers
