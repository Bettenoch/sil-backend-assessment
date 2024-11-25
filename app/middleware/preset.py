from dotenv import load_dotenv
import secrets
from typing import ClassVar, Literal
from pydantic_core import MultiHostUrl
from pydantic import (
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    setup_config: ClassVar[dict] = {
        "env_folder": ".env",
        "env_ignore_empty": True,
        "extra": "ignore",
    }
    
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str
    POSTGRES_DB: str = ""
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_PORT: int = 5432
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
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
    
settings = Settings()  # type: ignore
    