from volum.core.scene import SceneObject


class Plane(SceneObject):
    """Represents a plane in 3D space defined by a point and a normal vector."""
    def __init__(self, width:float , height: float):
        super().__init__()
        self.width = width
        self.height = height

    def to_dict(self):
        return {
            "type": "Plane",
            "width": self.width,
            "height": self.height
        }
    