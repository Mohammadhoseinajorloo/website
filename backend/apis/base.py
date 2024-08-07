from .v1 import route_task
from .v1 import route_login
from .v1 import route_user
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(route_user.router, prefix="", tags=["user"])
api_router.include_router(route_task.router, prefix="", tags=["task"])
api_router.include_router(route_login.router, prefix="", tags=["login"])
