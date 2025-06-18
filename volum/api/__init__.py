"""
API package for Volum: exposes a FastAPI application instance.
"""
import os
import json
import asyncio
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union

from .endpoints import router as scene_router
from .endpoints import observer, scene
from .utils import set_main_event_loop
from volum.config.runtime import runtime_config

#from volum.api.schema import ScenePayload, SceneObjectPayload
from volum.api.utils import create_scene_from_path


def load_and_watch():
    loop = asyncio.get_event_loop()
    set_main_event_loop(loop)

    if runtime_config.python_path:
        if os.path.isfile(runtime_config.python_path):
            async def start_initial_process():
                if runtime_config.python_path and os.path.isfile(runtime_config.python_path):
                    proc = await asyncio.create_subprocess_exec("python3", runtime_config.python_path)
                    await proc.communicate()
                    create_scene_from_path(str(runtime_config.scene_path))


            asyncio.get_event_loop().create_task(start_initial_process())
        else:
            raise FileNotFoundError(f"No such file: {runtime_config.python_path}")
    else:
        print("No PYTHON_PATH provided, skipping initial script execution.")

        # Initial load from disk
        if runtime_config.scene_path:
            create_scene_from_path(str(runtime_config.scene_path))
        else:
            raise ValueError("SCENE_PATH environment variable is not set and no Python script provided either.")

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
