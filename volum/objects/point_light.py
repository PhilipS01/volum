from numpy import linalg
from volum.core.scene import SceneObject

class PointLight(SceneObject):
    """Represents a point light in 3D space."""
    def __init__(self, intensity: float, color: str = "white"):
        super().__init__(material=None)  # PointLight does not have a material
        self._color = color
        self.intensity = intensity

    def to_dict(self):
        return {
            "type": "PointLight",
            "color": self.color,
            "intensity": self.intensity
        }
    
    @property
    def color(self):
        """Get the color of the point light."""
        return self._color
    
    @color.setter
    def color(self, value: str):
        """Set the color of the point light."""
        if not isinstance(value, str):
            raise TypeError(f"Expected color to be a string, got {type(value)}")
        self._color = value
    
    def distance_to(self, point):
        return linalg.norm(point)