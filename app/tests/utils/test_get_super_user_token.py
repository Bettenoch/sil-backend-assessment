#app/tests/utils/test_get_super_user_token.py

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.tests.utils.token_gen import get_superuser_headers


def test_get_superuser_headers():
    client = TestClient(app)

    # Mock settings values
    with patch("app.middleware.preset.settings") as mock_settings:
        mock_settings.FIRST_SUPERUSER_EMAIL = "bettenoch254@gmail.com"
        mock_settings.FIRST_SUPERUSER_PASSWORD = "bettex!254"
        mock_settings.API_V1_STR = "/sil/v1"

        # Send request using the function
        response_headers = get_superuser_headers(client)

        # Ensure the response returns a 200 status code
        response = client.post(
            f"{mock_settings.API_V1_STR}/login/authenticated_token",
            data={
                "username": mock_settings.FIRST_SUPERUSER_EMAIL,
                "password": mock_settings.FIRST_SUPERUSER_PASSWORD,
            },
        )
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

        # Validate the headers returned by the function
        assert "Authorization" in response_headers
        assert response_headers["Authorization"].startswith("Bearer ")
