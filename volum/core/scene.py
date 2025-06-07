from .registry import ObjectRegistry
import uuid

class Scene:
    def __init__(self):
        self.registry = ObjectRegistry()
        self.objects = {}

    def load_plugins(self, plugins):
        for plugin in plugins:
            plugin.register(self.registry)

    def add_object(self, obj_or_type, **kwargs):
        if isinstance(obj_or_type, str):
            cls = self.registry.get_type(obj_or_type)
            if cls is None:
                raise ValueError(f"Unknown object type: {obj_or_type}")
            obj = cls(**kwargs)
        else:
            obj = obj_or_type

        # ensure the object is a SceneObject
        if not isinstance(obj, SceneObject):
            raise TypeError(f"Object must be a SceneObject, got {type(obj)}")

        obj_id = str(len(self.objects)) or str(uuid.uuid4())
        setattr(obj, 'id', obj_id)  # set the id (SceneObject should provide an id attribute)
        self.objects[obj_id] = obj

    def serialize(self):
        return [obj.to_dict() for obj in self.objects.values()]
    

class SceneObject:
    def __init__(self, id=None):
        self.id = id

    def to_dict(self):
        raise NotImplementedError("SceneObject subclasses must implement a to_dict() method")