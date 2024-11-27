from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.middleware.preset import settings
from app.api.main import api_router


def generate_unique_id_for_route(route:APIRoute) -> str:
     return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title="SIL BACKEND ASSESSMENT",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=generate_unique_id_for_route,
)
app.include_router(api_router, prefix=settings.API_V1_STR)