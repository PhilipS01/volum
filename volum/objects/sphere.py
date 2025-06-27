import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial


class Sphere(SceneObject):
    """Represents a sphere in 3D space."""
    def __init__(self, radius, material: Optional[MeshMaterial]=None):
        if material is None:
            material = StandardMaterial()

        if not isinstance(material, MeshMaterial):
            raise TypeError(f"Sphere expects MeshMaterial, got {type(material)}")

        if not isinstance(radius, (int, float)) or radius <= 0:
            raise ValueError("Radius must be a positive number.")
        
        super().__init__(material)
        self.radius = radius

    def volume(self):
        return (4/3) * 3.14159 * (self.radius ** 3)

    def surface_area(self):
        return 4 * 3.14159 * (self.radius ** 2)

    def to_dict(self):
        return {
            "type": "Sphere",
            "radius": self.radius,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        radius = self.radius
        return max(0, np.linalg.norm(point) - radius)

    def __repr__(self):
        return f"Sphere(radius={self.radius}, material={self.material})"