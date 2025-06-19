from volum.core.scene import Scene
from volum.api.schema import ScenePayload, SceneObjectPayload
from volum.core.builder import build_object_from_dict
from volum.plugins.base_shapes import BaseShapesPlugin

# load your plugins
from volum.plugins.base_shapes import BaseShapesPlugin
from volum.plugins.lights import LightsPlugin
#from plugins.data_plots import DataPlotsPlugin


# Initialize global Scene and registry
scene = Scene()
scene.load_plugins([BaseShapesPlugin(), LightsPlugin()]) # need to load plugins for the API scene object as well (loading them from the user's script is not enough)

def create_scene(payload: ScenePayload):
    """Create a new scene from the provided payload.

    Args:
        payload (ScenePayload): The payload containing scene data.

    Returns:
        dict: A dictionary containing the status and object count.
    """

    scene.clear()
    for obj_def in payload.objects:
        obj_dict = obj_def.model_dump(exclude_none=True)
        # Use builder to instantiate Python object
        obj = build_object_from_dict(obj_dict, scene.registry)
        scene.add_object(obj)

    return {"status": "ok", "object_count": len(scene.objects)}