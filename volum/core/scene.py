from volum.core.registry import ObjectRegistry
from volum.core.plugin import ScenePlugin

from typing import List, Dict, Any, Union
import uuid, os, numpy as np

from volum.core.interfaces import Serializable


class Scene:
    def __init__(self):
        self.registry = ObjectRegistry()
        self.plugins: List[ScenePlugin] = []
        self.objects: Dict[str, Any] = {}

    def load_plugins(self, plugins: List[ScenePlugin]):
        """Load plugins into the scene's registry."""
        for plugin in plugins:
            if not isinstance(plugin, ScenePlugin):
                raise TypeError(f"Expected ScenePlugin, got {type(plugin)}")
            if plugin not in self.plugins:
                plugin.register(self.registry)
                self.plugins.append(plugin)

    def add_object(self, obj_or_type, **kwargs):
        if isinstance(obj_or_type, str):
            cls = self.registry.get_type(obj_or_type)
            if cls is None:
                raise ValueError(f"Unknown object type: {obj_or_type}")
            obj = cls(**kwargs)
        else:
            obj = obj_or_type

        # Ensure the object is a SceneObject
        if not isinstance(obj, SceneObject):
            raise TypeError(f"Object must be a SceneObject, got {type(obj)}")

        obj_id = str(len(self.objects)) or str(uuid.uuid4())
        setattr(obj, 'id', obj_id)  # set the id (SceneObject should provide an id attribute)
        self.objects[obj_id] = obj

    def serialize(self):
        return {
            "plugins": [plugin.name for plugin in self.plugins],
            "objects": [obj.to_dict() for obj in self.objects.values()]
        }

    def clear(self):
        """Clear all objects in the scene."""
        self.objects.clear()

    def save(self, path: str=os.path.join(os.getcwd(), "scene.json")):
        """Save the current scene to a JSON file."""
        import json
        with open(path, 'w') as f:
            json.dump(self.serialize(), f, indent=2)


class SceneObject(Serializable):
    def __init__(self, id=None):
        self.id = id
    
    def distance_to(self, point: Union[List[float], np.ndarray, tuple]):
        raise NotImplementedError("SceneObject subclasses must implement a distance() method")