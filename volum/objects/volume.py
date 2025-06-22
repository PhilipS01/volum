import numpy as np
from volum.core.scene import SceneObject

class Volume(SceneObject):
    """Represents a 3D volume object via a file path."""
    def __init__(self, width: float, height: float, depth: float, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.width = width
        self.height = height
        self.depth = depth

    def to_dict(self):
        return {
            "type": "Volume",
            "file_path": self.file_path,
            "width": self.width,
            "height": self.height,
            "depth": self.depth,
        }
    
    def distance_to(self, point):
        # Bounding box distance calculation
        half_extents = np.array([self.width, self.height, self.depth]) * 0.5
        clamped = np.maximum(np.abs(point) - half_extents, 0)
        return np.linalg.norm(clamped)

    def __repr__(self):
        return f"Volume(file_path={self.file_path}, width={self.width}, height={self.height}, depth={self.depth})"