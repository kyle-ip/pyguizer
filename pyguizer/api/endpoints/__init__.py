"""API endpoints for PyGUIzer"""

from fastapi import APIRouter

from pyguizer.api.endpoints import functions, pipelines, presets, tasks

# Create main router
api_router = APIRouter()

# Include all routers
api_router.include_router(functions.router)
api_router.include_router(tasks.router)
api_router.include_router(presets.router)
api_router.include_router(pipelines.router)

__all__ = ["api_router"]
