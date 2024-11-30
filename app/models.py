#models.py

from typing import List, Optional
import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


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
    albums : list["Album"] = Relationship(back_populates="owner", cascade_delete=True)
    photos: list["Photo"] = Relationship(back_populates="owner", cascade_delete=True)
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


#-------------------AlBUMS-----------------#

class AlbumBase(SQLModel):
    title: str = Field( min_length=1,max_length=255, default=None)
    description: str | None = Field(max_length=1000, default=None)
    cover_photo: Optional[str] = Field(max_length=1000, default="https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=1798&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    
class AlbumCreate(AlbumBase):
    pass

class AlbumUpdate(AlbumBase):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)  # type: ignore
    
class Album(AlbumBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True, max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" = Relationship(back_populates="albums")
    photos: list["Photo"] = Relationship(back_populates="album", cascade_delete=True)
    
class AlbumPublic(AlbumBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
class AlbumsPublic(SQLModel):
    data: List[AlbumPublic]
    count: int
    
#-------------------PHOTOS-----------------#

class PhotoBase(SQLModel):
    photo_title: str= Field( min_length=1,max_length=255, default=None),
    image_url: str = Field(max_length=355, default=None)
    
    
class PhotoCreate(PhotoBase):
    album_id: uuid.UUID

class PhotoUpdate(SQLModel):
    photo_title: str | None= Field( min_length=1,max_length=255, default=None),
    image_url: str | None = Field(min_length=1, max_length=355, default=None)
    
    
class Photo(PhotoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    photo_title: str = Field(index=True, max_length=255)  # Add index to photo_title
    image_url: str = Field(max_length=355, default=None)
    album_id: uuid.UUID = Field(foreign_key="album.id", nullable=False, ondelete="CASCADE")
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    owner: "User" = Relationship(back_populates="photos")
    album: "Album" = Relationship(back_populates="photos")
    
class PhotoPublic(PhotoBase):
    id: uuid.UUID
    album_id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
class PhotosPublic(SQLModel):
    data: List[PhotoPublic]
    count: int