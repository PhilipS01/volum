from volum.core.registry import ObjectRegistry, MaterialInstances
from volum.core.plugin import ScenePlugin

from typing import List, Dict, Union
import uuid, os, numpy as np

from volum.core.interfaces import Serializable
from volum.core.materials import Material


class Scene:
    def __init__(self):
        self.registry = ObjectRegistry()
        self.plugins: List[ScenePlugin] = []
        self.objects: Dict[str, SceneObject] = {}
        self.materials = MaterialInstances()

    def load_plugins(self, plugins: List[ScenePlugin]):
        """Load plugins into the scene's registry."""
        for plugin in plugins:
            if not isinstance(plugin, ScenePlugin):
                raise TypeError(f"Expected ScenePlugin, got {type(plugin)}")
            if plugin not in self.plugins:
                plugin.register(self.registry)
                self.plugins.append(plugin)

    def add_object(self, obj_or_type: Union[str, "SceneObject", Material], **kwargs):
        """Add an object to the scene.

        Args:
            obj_or_type (Union[str, SceneObject, Material]): The object or type of object to add.

        Raises:
            ValueError: If the object type is unknown.
            TypeError: If the object is not a SceneObject or Material.
        """

        # TODO: support material as plugin
        # TODO: support color as single argument (overrides material color or defaults to StandardMaterial)
        if isinstance(obj_or_type, str):
            cls = self.registry.get_type(obj_or_type)
            if cls is None:
                raise ValueError(f"Unknown object type: {obj_or_type}")
            
            if isinstance(kwargs.get("material", None), str):
                kwargs["scene"] = self  # pass scene to resolve material by name

            obj = cls(**kwargs)
        else:
            obj = obj_or_type

        # Ensure the object is a SceneObject
        if not isinstance(obj, SceneObject) and not isinstance(obj, Material):
            raise TypeError(f"Object must be a SceneObject or Material, got {type(obj)}")

        if isinstance(obj, Material):
            obj_id = obj.name
            if obj_id is None:
                raise ValueError("Material must be added with a 'name' kwarg to the scene.")
            self.materials.register_material(obj_id, obj)
        else:
            obj_id = f"{len(self.objects)}-{uuid.uuid4()}"
            setattr(obj, '_id', obj_id) # set the id (SceneObject should provide an id attribute)
            self.objects[obj_id] = obj

    def serialize(self):
        """Serialize the scene to a dictionary."""
        return {
            "plugins": [plugin.name for plugin in self.plugins],
            "objects": [obj.to_dict() for obj in self.objects.values()] + [mat.to_dict() for mat in self.materials.materials.values()],
        }

    def clear(self):
        """Clear all objects and materials in the scene. Does not remove plugins."""
        self.objects.clear()
        self.materials.clear()

    def save(self, path: str=os.path.join(os.getcwd(), "scene.json")):
        """Save the current scene to a JSON file."""
        import json
        with open(path, 'w') as f:
            json.dump(self.serialize(), f, indent=2)

    def __getitem__(self, key: str):
        """Get a scene object by its ID. Not including materials."""
        return self.objects.get(key)


class SceneObject(Serializable):
    _material: Material

    def __init__(self, material, id=None, **kwargs):
        if isinstance(material, str):
            # If material is a string, assume it's a material name and fetch it from the scene
            scene = kwargs.get('scene', None)
            if isinstance(scene, Scene):
                if material in scene.materials:
                    mat = scene.materials.get_material(material)
                    if mat is None:
                        raise ValueError(f"Material '{material}' not found in the scene materials.")
                    else:
                        self._material = mat
                else:
                    raise ValueError(f"Material '{material}' not found in the scene materials.")
            else:
                raise ValueError("Scene must be provided to resolve material by name (as kwarg in the SceneObject constructor).")
        elif isinstance(material, Material):
            self._material = material
        else:
            self._material = None # type: ignore (for special objects without material, e.g. PointLight)

        self._id = id

    @property
    def material(self) -> Material:
        """Get the material of the object."""
        return self._material
    
    @material.setter
    def material(self, value: Material):
        """Set the material of the object."""
        if not isinstance(value, Material):
            raise TypeError(f"Expected Material, got {type(value)}")
        self._material = value

    @property
    def color(self) -> Union[str, None]:
        """Get the color of the object's material."""
        return self._material.color if self._material else None
    
    @color.setter
    def color(self, value: str):
        """Set the color of the object's material."""
        if self._material:
            self._material.color = value
        else:
            raise ValueError("Cannot set color on an object without a material")
        
    @property
    def id(self) -> str:
        """Get the unique identifier of the SceneObject."""
        if self._id is None:
            raise ValueError("Object ID is not set. Ensure to set 'id' in the constructor or use 'set_id()'.")
        return self._id

    def distance_to(self, point: Union[List[float], np.ndarray, tuple]):
        raise NotImplementedError("SceneObject subclasses must implement a distance() method")
    
    def transform(self, position=None, rotation=None, scale=None):
        """Apply a transformation to the object."""
        from volum.objects.transform import Transform
        return Transform(object=self, position=position, rotation=rotation, scale=scale)
    