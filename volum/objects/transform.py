from ..core.scene import SceneObject

class Transform(SceneObject):
    """Represents a transformation applied to a SceneObject, including position, rotation, and scale."""
    def __init__(self, object: SceneObject, position=None, rotation=None, scale=None):
        
        if not isinstance(object, SceneObject):
            raise TypeError(f"{object} is not a SceneObject.")
        
        super().__init__()
        self.object = object
        self.position = position or [0, 0, 0]
        self.rotation = rotation or [0, 0, 0]
        self.scale = scale or [1, 1, 1]

    def to_dict(self):
        return {
            "type": "Transform",
            "position": self.position,
            "rotation": self.rotation,
            "scale": self.scale,
            "child": self.object.to_dict()
        }
    