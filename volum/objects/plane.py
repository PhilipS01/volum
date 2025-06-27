import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial


class Plane(SceneObject):
    """Represents a plane in 3D space defined by a point and a normal vector."""
    def __init__(self, width:float , height: float, material: Optional[MeshMaterial]=None):
        if material is None:
            material = StandardMaterial()
            
        if not isinstance(material, MeshMaterial):
            raise TypeError(f"Plane expects MeshMaterial, got {type(material)}")

        super().__init__(material)
        self.width = width
        self.height = height

    def to_dict(self):
        return {
            "type": "Plane",
            "width": self.width,
            "height": self.height,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        half_w = self.width / 2
        half_d = self.height / 2

        px, py, pz = point
        clamped_x = np.clip(px, -half_w, half_w)
        clamped_z = np.clip(pz, -half_d, half_d)

        # Closest point on the rectangle in local space
        closest = np.array([clamped_x, 0.0, clamped_z])
        dist_vector = np.array([px, py, pz]) - closest
        return np.linalg.norm(dist_vector)
    
    def __repr__(self):
        return f"Plane(width={self.width}, height={self.height}, material={self.material})"