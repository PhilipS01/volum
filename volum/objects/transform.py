from core.scene import SceneObject

class Transform(SceneObject):
    """Represents a transformation applied to a SceneObject, including position, rotation, and scale."""
    def __init__(self, target: SceneObject, position=None, rotation=None, scale=None):
        
        if not isinstance(target, SceneObject):
            raise TypeError(f"{target} is not a SceneObject.")
        
        super().__init__()
        self.target = target
        self.position = position or [0, 0, 0]
        self.rotation = rotation or [0, 0, 0]
        self.scale = scale or [1, 1, 1]

    def to_dict(self):
        return {
            "type": "Transform",
            "position": self.position,
            "rotation": self.rotation,
            "scale": self.scale,
            "child": self.target.to_dict()
        }
    