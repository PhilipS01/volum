import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial

class Box(SceneObject):
    """Represents a box in 3D space."""
    def __init__(self, width: float, height: float, depth: float, material: Optional[MeshMaterial]=None):
        if material is None:
            material = StandardMaterial()
            
        if not isinstance(material, MeshMaterial):
            raise TypeError(f"Box expects MeshMaterial, got {type(material)}")

        super().__init__(material)
        self.width = width
        self.height = height
        self.depth = depth

    def to_dict(self):
        return {
            "type": "Box",
            "width": self.width,
            "height": self.height,
            "depth": self.depth,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        half_extents = np.array([self.width, self.height, self.depth]) * 0.5
        clamped = np.maximum(np.abs(point) - half_extents, 0)
        return np.linalg.norm(clamped)
    
    def __repr__(self):
        return f"Box(width={self.width}, height={self.height}, depth={self.depth}"