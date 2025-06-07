from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

from core.scene import Scene
from core.builder import build_object_from_dict
# load your plugins
from plugins.base_shapes import BaseShapesPlugin
#from plugins.data_plots import DataPlotsPlugin

router = APIRouter()

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
    for obj in scene.objects:
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
