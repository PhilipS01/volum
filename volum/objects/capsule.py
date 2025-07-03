import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial

class Capsule(SceneObject):
    """Represents a capsule in 3D space."""
    def __init__(self, radius: float, height: float, cap_segments: int = 10, radial_segments: int = 20, material: Optional[MeshMaterial] = None):
        if material is None:
            material = StandardMaterial()
            
        if not isinstance(material, MeshMaterial):
            raise TypeError(f"Box expects MeshMaterial, got {type(material)}")

        super().__init__(material)
        self.radius = radius
        self.height = height
        self.cap_segments = cap_segments
        self.radial_segments = radial_segments

    def to_dict(self):
        return {
            "type": "Capsule",
            "radius": self.radius,
            "height": self.height,
            "cap_segments": self.cap_segments,
            "radial_segments": self.radial_segments,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        y = point[1]
        xz_dist = np.linalg.norm(np.array(point)[[0, 2]])

        # Compute radial and vertical distances
        radial_dist = max(0, xz_dist - self.radius)
        y_dist = max(0, abs(y) - self.height / 2)

        return np.linalg.norm(np.array([radial_dist, y_dist]))
    
    def __repr__(self):
        return f"Capsule(radius={self.radius}, height={self.height}, cap_segments={self.cap_segments}, radial_segments={self.radial_segments}, material={self.material})"