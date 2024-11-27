#app/middleware/user_auth.py

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app.middleware.preset import settings

ALGO = "HS256"


spawn_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return spawn_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return spawn_context.verify(plain_password, hashed_password)


def create_token_access(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGO)
    return encoded_jwt
