import os, json, time

from volum.api.schema import ScenePayload, SceneObjectPayload
from volum.api.scene import scene, create_scene
from volum.config.runtime import runtime_config


_main_loop = None

def set_main_event_loop(loop):
    global _main_loop
    _main_loop = loop

def get_main_event_loop():
    return _main_loop

def _safe_json_load(path, retries=10, delay=0.5):
    for i in range(retries):
        try:
            if os.path.getsize(path) == 0:
                raise ValueError("File is empty")

            with open(path, "r") as f:
                return json.load(f)

        except (json.JSONDecodeError, ValueError):
            time.sleep(delay)
    raise RuntimeError(f"Failed to load JSON from {path} after {retries} retries. Maybe file is still being written because of the size?")

def create_scene_from_path(path: str):
    if path and os.path.isfile(path):
        data = _safe_json_load(path)
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