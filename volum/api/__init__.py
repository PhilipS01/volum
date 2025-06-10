"""
API package for Volum: exposes a FastAPI application instance.
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .endpoints import router as scene_router

app = FastAPI(
    title="Volum API",
    description="RESTful API to create, update, and retrieve Volum 3D scenes",
    version="0.1.0"
)

app.include_router(scene_router, prefix="/api/scene", tags=["scene"])

viewer_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "viewer", "public"))
app.mount("/", StaticFiles(directory=viewer_path, html=True), name="viewer")

__all__ = ["app"]
