from numpy import linalg
from volum.core.scene import SceneObject

class PointLight(SceneObject):
    """Represents a point light in 3D space."""
    def __init__(self, intensity: float, color: str = "white"):
        super().__init__()
        self.color = color
        self.intensity = intensity

    def to_dict(self):
        return {
            "type": "PointLight",
            "color": self.color,
            "intensity": self.intensity
        }
    
    def distance_to(self, point):
        return linalg.norm(point)