"""
API package for Volum: exposes a FastAPI application instance.
"""
import os
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from .endpoints import ScenePayload, router as scene_router
from .endpoints import observer, scene, SCENE_PATH, create_scene


def load_and_watch():
    # Initial load from disk
    if SCENE_PATH:
        if os.path.isfile(SCENE_PATH):
            with open(SCENE_PATH, "r") as f:
                data = json.load(f)
            scene.clear()
            # Create a ScenePayload from the loaded data
            if isinstance(data, list):
                payload = ScenePayload(objects=data)
            elif isinstance(data, dict):
                payload = ScenePayload(**data)
            else:
                raise ValueError("Invalid scene data format")
            # Create the scene with the loaded data
            create_scene(payload)
        else:
            raise FileNotFoundError(f"Scene file not found: {SCENE_PATH}")

    # Start the watchdog observer
    observer.start()

def cleanup_observer():
    # Stop and join the watcher cleanly
    observer.stop()
    observer.join()

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_and_watch()
    yield
    cleanup_observer()

app = FastAPI(
    title="Volum API",
    description="RESTful API to create, update, and retrieve Volum 3D scenes",
    version="0.1.0",
    lifespan=lifespan
)

# Include the scene router for handling scene-related endpoints
app.include_router(scene_router, prefix="/api/scene", tags=["scene"])

# Serve the index.html file for the viewer
public_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "viewer", "public"))
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(public_path, "index.html"))

@app.get("/favicon.ico")
def favicon():
    return FileResponse(os.path.join(public_path, "favicon.ico"))

# Serve static files for the viewer
static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "viewer", "src"))
app.mount("/static", StaticFiles(directory=static_path, html=True), name="viewer")

__all__ = ["app"]
