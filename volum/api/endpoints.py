import os, asyncio, time, hashlib
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, FastAPI
from fastapi.responses import FileResponse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from volum.api.schema import ScenePayload, SceneObjectPayload
from volum.api.scene import scene, create_scene
from volum.api.utils import get_main_event_loop
from volum.api.utils import create_scene_from_path

from volum.config.runtime import runtime_config
from volum.config.constants import TerminalColors


router = APIRouter()

# Paths from runtime config
SCENE_PATH = runtime_config.scene_path
PYTHON_PATH = runtime_config.python_path


@router.post("/", summary="Create or replace the entire scene")
def create_scene(payload: ScenePayload):
    return create_scene(payload)

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
    def __init__(self, scene_path: str, event_name: str, python_path: Optional[str] = None):
        self.scene_path = os.path.abspath(scene_path)
        self.event_name = event_name
        self.python_path = os.path.abspath(python_path) if (python_path and os.path.isfile(python_path)) else None
        self._last_hashes = {}  # key: file path, value: hash
        self._debounce_seconds = .5  # tune as needed
        self._last_modified_times = {}

    def _file_hash(self, path: str) -> str:
        try:
            with open(path, "rb") as f:
                return hashlib.sha1(f.read()).hexdigest()
        except FileNotFoundError:
            return ""

    def on_modified(self, event: FileSystemEvent):
        if event.is_directory:
            return  # Ignore directory events
    
        path = os.path.abspath(event.src_path)
        now = time.time()

        last_time = self._last_modified_times.get(path, 0)
        if now - last_time < self._debounce_seconds:
            return
        self._last_modified_times[path] = now

        current_hash = self._file_hash(str(path))
        last_hash = self._last_hashes.get(path, "")
        if current_hash == last_hash:
            return  # no actual content change

        self._last_hashes[path] = current_hash

        loop = get_main_event_loop()
        if not loop:
            raise RuntimeError("Main event loop is not set.")
        
        if path == self.scene_path:
            if runtime_config.debug:
                print(f"{TerminalColors.INFO}{self.scene_path.split()[-1]}, modified scene file, reloading ...{TerminalColors.RESET}")
            
            create_scene_from_path(str(self.scene_path))
            asyncio.run_coroutine_threadsafe(manager.broadcast(self.event_name), loop)

        if self.python_path and path == self.python_path: # usually happens first, this will change the file under scene_path and trigger the broadcast (see above)
            if runtime_config.debug:
                print(f"{TerminalColors.INFO}{self.python_path.split()[-1]}, modified python file, reloading ...{TerminalColors.RESET}")

            async def restart_script():
                if self.python_path:
                    proc = await asyncio.create_subprocess_exec("python3", self.python_path)
                    await proc.communicate()

            asyncio.run_coroutine_threadsafe(restart_script(), loop)


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            # Just keep the connection alive
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)

# Initialize the connection manager and observer
manager = ConnectionManager()
observer = Observer()

# Start observing the scene file if provided
if SCENE_PATH and PYTHON_PATH is None:
    observer.schedule(
        LiveFileHandler(str(SCENE_PATH),  "scene_updated"),
        os.path.dirname(SCENE_PATH), recursive=False
    )
    
if SCENE_PATH and PYTHON_PATH is not None:
    observer.schedule(
        LiveFileHandler(str(SCENE_PATH), "scene_updated", python_path=str(PYTHON_PATH)),
        os.path.dirname(SCENE_PATH), recursive=False
    )
