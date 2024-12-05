from fastapi import APIRouter

from app.api.routes import (
    albums,
    get_album_photos,
    get_all_photos,
    get_user_albums,
    health_check,
    login,
    photos,
    users,
)

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(albums.router, prefix="/albums", tags=["albums"])
api_router.include_router(
    get_user_albums.router, prefix="/users/{user_id}/album", tags=["user_albums"]
)
api_router.include_router(photos.router, prefix="/photos", tags=["photos"])
api_router.include_router(
    get_album_photos.router,
    prefix="/users/{user_id}/albums/{album_id}/photos",
    tags=["all_album_photos"],
)

api_router.include_router(
    get_all_photos.router,
    prefix="/all_photos",
    tags=["all_photos"],
)
api_router.include_router(health_check.router, prefix="/health", tags=["health"])
