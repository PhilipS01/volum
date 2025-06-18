import os, json

from volum.api.scene import scene, create_scene
from volum.api.schema import ScenePayload, SceneObjectPayload
from volum.config.runtime import runtime_config


_main_loop = None

def set_main_event_loop(loop):
    global _main_loop
    _main_loop = loop

def get_main_event_loop():
    return _main_loop

def create_scene_from_path(path: str):
    if path and os.path.isfile(path):
        with open(path, "r") as f:
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
        raise FileNotFoundError(f"No such file: {runtime_config.scene_path}")