class ObjectRegistry:
    """A registry for storing and retrieving object types."""
    def __init__(self):
        self.types = {}

    def register_type(self, name, cls):
        self.types[name] = cls

    def get_type(self, name):
        return self.types.get(name)