import secrets
from typing import ClassVar, Literal

from dotenv import load_dotenv
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    setup_config: ClassVar[dict[str, str | int | bool]] = {
        "env_folder": ".env",
        "env_ignore_empty": True,
        "extra": "ignore",
    }

    SECRET_KEY: str = secrets.token_urlsafe(32)

    API_V1_STR: str = "/sil/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    # db credentials
    PROJECT_NAME: str
    POSTGRES_DB: str = ""
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_PORT: int = 5432

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_NAME: str
    FIRST_SUPERUSER_USERNAME: str

    EMAIL_TEST_USER: str = "test@example.com"


settings = Settings()  # type: ignore
