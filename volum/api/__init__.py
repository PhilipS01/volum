"""
API package for Volum: exposes a FastAPI application instance.
"""
from fastapi import FastAPI
from .endpoints import router as scene_router

app = FastAPI(
    title="Volum API",
    description="RESTful API to create, update, and retrieve Volum 3D scenes",
    version="0.1.0"
)

# Mount the scene router at /scene
app.include_router(scene_router, prefix="/scene", tags=["scene"])

__all__ = ["app"]
