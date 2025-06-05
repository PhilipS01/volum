from .registry import ObjectRegistry

class Scene:
    def __init__(self):
        self.registry = ObjectRegistry()
        self.objects = []

    def load_plugins(self, plugins):
        for plugin in plugins:
            plugin.register(self.registry)

    def add_object(self, type_name, **kwargs):
        cls = self.registry.get_type(type_name)
        if cls is None:
            raise ValueError(f"Unknown object type: {type_name}")
        obj = cls(**kwargs)
        self.objects.append(obj)

    def serialize(self):
        return [obj.to_dict() for obj in self.objects]