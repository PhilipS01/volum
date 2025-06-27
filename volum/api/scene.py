from volum.core.scene import Scene
from volum.api.schema import ScenePayload
from volum.core.builder import build_object_from_dict
# load your plugins
from volum.plugins import PLUGIN_MAP

from volum.config.runtime import runtime_config
from volum.config.constants import TerminalColors


scene = Scene() # initialize global Scene and registry

def create_scene(payload: ScenePayload):
    """Create a new scene from the provided payload.

    Args:
        payload (ScenePayload): The payload containing scene data.

    Returns:
        dict: A dictionary containing the status and object count.
    """

    plugins = []
    for plugin_name in payload.plugins:
        plugin_cls = PLUGIN_MAP.get(plugin_name, None)
        if plugin_cls is not None:
            plugins.append(plugin_cls())
    
    scene.load_plugins(plugins)

    scene.clear()
    for obj_def in payload.objects:
        obj_dict = obj_def.model_dump(exclude_none=True)
        # Use builder to instantiate Python object
        obj = build_object_from_dict(obj_dict, scene.registry)
        
        if runtime_config.debug:
            print(f"{TerminalColors.INFO}Adding object{TerminalColors.RESET} of type {TerminalColors.BOLD}{obj.__class__.__name__}{TerminalColors.RESET}: {obj.to_dict()}")
        
        scene.add_object(obj)

    return {"status": "ok", "object_count": len(scene.objects), "plugins": plugins}