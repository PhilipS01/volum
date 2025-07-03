import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial

class Circle(SceneObject):
    """Represents a circle in 3D space."""
    def __init__(self, radius: float, segments: int = 32, perimeter: float = 2*np.pi, perimeter_start: float = 0, material: Optional[MeshMaterial] = None):
        if material is None:
            material = StandardMaterial()
            
        if not isinstance(material, MeshMaterial):
            raise TypeError(f"Circle expects MeshMaterial, got {type(material)}")

        super().__init__(material)
        self.radius = radius
        self.segments = segments
        self.perimeter = perimeter
        self.perimeter_start = perimeter_start

    def to_dict(self):
        return {
            "type": "Circle",
            "radius": self.radius,
            "segments": self.segments,
            "perimeter": self.perimeter,
            "perimeter_start": self.perimeter_start,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        px, py, pz = point
        r_vec = np.array([px, 0, pz])
        r_len = np.linalg.norm(r_vec)

        # Clamp to the circle's edge if outside
        if r_len > self.radius:
            r_vec = r_vec * (self.radius / r_len)

        closest = np.array([r_vec[0], 0, r_vec[2]])  # y = 0 plane
        dist_vector = np.array([px, py, pz]) - closest
        return np.linalg.norm(dist_vector)
    
    def __repr__(self):
        return f"Circle(radius={self.radius}, segments={self.segments}, perimeter={self.perimeter}, perimeter_start={self.perimeter_start}, material={self.material})"