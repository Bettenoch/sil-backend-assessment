from fastapi import APIRouter

from app.api.routes import health_check, login, users

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(health_check.router, prefix="/health", tags=["health"])
