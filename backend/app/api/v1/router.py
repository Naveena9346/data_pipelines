from fastapi import APIRouter
from app.api.v1 import auth, sources, pipelines, executions, monitoring

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(sources.router)
api_router.include_router(pipelines.router)
api_router.include_router(executions.router)
api_router.include_router(monitoring.router)
