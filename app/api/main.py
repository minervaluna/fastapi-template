from fastapi import APIRouter

from app.api.routes import user, file, token

api_router = APIRouter()
api_router.include_router(token.router)
api_router.include_router(user.router)
api_router.include_router(file.router)
