from ..core.scene import SceneObject


class Sphere(SceneObject):
    """Represents a sphere in 3D space."""
    def __init__(self, radius, color: str = "gray"):
        super().__init__()
        self.radius = radius
        self.color = color

    def volume(self):
        return (4/3) * 3.14159 * (self.radius ** 3)

    def surface_area(self):
        return 4 * 3.14159 * (self.radius ** 2)

    def to_dict(self):
        return {
            "type": "Sphere",
            "radius": self.radius,
            "color": self.color
        }
    