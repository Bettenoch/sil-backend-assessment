import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str = Field(default=None, max_length=255)
    username: str = Field(unique=True, index=True, default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_superuser: bool = False
    is_active: bool = True
    avatar: str | None = Field(
        default="https://gravatar.com/avatar/665f4ef319bd291a2a453464c723481c?s=400&d=robohash&r=x",
        max_length=1000,
    )


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    name: str = Field(default=None, max_length=255)
    username: str = Field(default=None, max_length=255)
    avatar: str | None = Field(
        default="https://gravatar.com/avatar/665f4ef319bd291a2a453464c723481c?s=400&d=robohash&r=x",
        max_length=1000,
    )


class UserUpdate(UserBase):
    password: str | None = Field(default=None, min_length=8, max_length=40)
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore


class UserUpdateMe(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    username: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(max_length=255)


class UpdatePassword(SQLModel):
    initial_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None
