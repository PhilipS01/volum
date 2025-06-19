from volum.core.scene import SceneObject

class Line(SceneObject):
    """Represents a line segment in 3D space."""
    def __init__(self, start: list, end: list):
        super().__init__()
        self.start = start  # Start point of the line
        self.end = end      # End point of the line

    def length(self):
        """Calculate the length of the line."""
        return ((self.end[0] - self.start[0]) ** 2 + 
                (self.end[1] - self.start[1]) ** 2 + 
                (self.end[2] - self.start[2]) ** 2) ** 0.5

    def to_dict(self):
        return {
            "type": "Line",
            "start": self.start,
            "end": self.end
        }
    