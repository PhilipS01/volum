from core.interfaces import Serializable

class Box(Serializable):
    """Represents a box in 3D space."""
    def __init__(self, width: float, height: float, depth: float, color: str = "gray"):
        self.width = width
        self.height = height
        self.depth = depth
        self.color = color

    def to_dict(self):
        return {
            "type": "Box",
            "width": self.width,
            "height": self.height,
            "depth": self.depth,
            "color": self.color
        }