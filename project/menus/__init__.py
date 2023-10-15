from fastapi import APIRouter

api_v1_router = APIRouter(
    prefix="/api/v1",
)

from . import models, tasks
