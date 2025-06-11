import os
import json
import asyncio
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from core.scene import Scene
from core.builder import build_object_from_dict
# load your plugins
from plugins.base_shapes import BaseShapesPlugin
#from plugins.data_plots import DataPlotsPlugin

router = APIRouter()

# Read watched file paths from env vars (set by run_live.py)
SCENE_PATH  = os.getenv("SCENE_PATH")

# Initialize global Scene and registry
scene = Scene()
scene.load_plugins([BaseShapesPlugin()])

class SceneObjectPayload(BaseModel):
    type: str = Field(..., description="Registered object type name")
    # Optional fields for object properties
    object: Optional[Dict[str, Any]] = None
    position: Optional[List[float]] = None
    rotation: Optional[List[float]] = None
    scale: Optional[List[float]] = None
    color: Optional[List[float]] = None
    # Capture any additional fields (that may be defined by plugins)
    class Config:
        extra = 'allow'

class ScenePayload(BaseModel):
    objects: List[SceneObjectPayload]

@router.post("/", summary="Create or replace the entire scene")
def create_scene(payload: ScenePayload):
    # Clear existing
    scene.objects.clear()

    for obj_def in payload.objects:
        obj_dict = obj_def.model_dump(exclude_none=True)
        # Use builder to instantiate Python object
        obj = build_object_from_dict(obj_dict, scene.registry)
        scene.add_object(obj)

    return {"status": "ok", "object_count": len(scene.objects)}

@router.get("/", summary="Get the current scene as JSON")
def get_scene():
    serialized = []
    for obj in scene.objects.values():
        d = obj.to_dict()
        obj_id = getattr(obj, 'id', None)
        if obj_id:
            d['id'] = obj_id # expose the id
        serialized.append(d)
    return {"objects": serialized}

@router.put("/object/{object_id}", summary="Update a single object by ID")
def update_object(object_id: str, update: SceneObjectPayload):
    obj = scene.objects.get(object_id)
    if not obj:
        raise HTTPException(404, "Object not found")

    updates = update.model_dump(exclude_none=True, exclude={'type'})
    for k, v in updates.items():
        setattr(obj, k, v)

    return {"status": "ok", "id": object_id}

@router.delete("/", summary="Clear the scene")
def delete_scene():
    scene.objects.clear()
    return {"status": "ok"}


# Manage WebSocket connections for live updates
class ConnectionManager:
    def __init__(self):
        self.active: set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.add(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, message: str):
        for ws in list(self.active):
            try:
                await ws.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(ws)

# Watchdog File Handler
class LiveFileHandler(FileSystemEventHandler):
    def __init__(self, path: str, event_name: str):
        self.watch_path = os.path.abspath(path)
        self.event_name = event_name

    def on_modified(self, event):
        if os.path.abspath(event.src_path) == self.watch_path:
            # schedule a broadcast on the event loop
            asyncio.get_event_loop().create_task(
                manager.broadcast(self.event_name)
            )

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            # Just keep the connection alive
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)


manager = ConnectionManager()
observer = Observer()
# Start observing the scene file if provided
if SCENE_PATH:
    observer.schedule(
        LiveFileHandler(SCENE_PATH,  "scene_updated"),
        os.path.dirname(SCENE_PATH), recursive=False
    )

observer.start()