from fastapi import APIRouter

from app.api.routes import albums, get_album_photos, get_user_albums, health_check, login, photos, users

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(albums.router, prefix="/albums", tags=["albums"])
api_router.include_router(get_user_albums.router, prefix="/user_albums", tags=["user_albums"])
api_router.include_router(photos.router, prefix="/photos", tags=["photos"])
api_router.include_router(get_album_photos.router, prefix="/album_photos", tags=["album_photos"])
api_router.include_router(health_check.router, prefix="/health", tags=["health"])

