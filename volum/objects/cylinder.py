import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial

class Cylinder(SceneObject):
    """Represents a cylinder object in the scene."""
    def __init__(self, radius_top: float, radius_bottom: float, height: float, radial_segments: int = 64, material: Optional[MeshMaterial] = None, **kwargs):
        if material is None:
            material = StandardMaterial()

        if not isinstance(material, MeshMaterial):
            raise TypeError(f"Cylinder expects MeshMaterial, got {type(material)}")

        super().__init__(material, **kwargs)
        self.radius_top = radius_top
        self.radius_bottom = radius_bottom
        self.height = height
        self.radial_segments = radial_segments

    def volume(self):
        from math import pi
        return 1/3 * pi * self.height * (self.radius_top**2 + self.radius_bottom**2 + self.radius_bottom*self.radius_bottom)

    def surface_area(self):
        from math import pi
        return pi * (self.radius_top + self.radius_bottom) * ((self.radius_top - self.radius_bottom)**2 + self.height**2)**0.5 + pi * (self.radius_top**2 + self.radius_bottom**2)

    def to_dict(self):
        return {
            "type": "Cylinder",
            "radius_top": self.radius_top,
            "radius_bottom": self.radius_bottom,
            "height": self.height,
            "radial_segments": self.radial_segments,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        y = point[1]
        xz_dist = np.linalg.norm(np.array(point)[[0, 2]])

        # Clamp Y to the height range
        y_clamped = np.clip(y, -self.height / 2, self.height / 2)

        # Interpolate radius at this Y height
        t = (y_clamped + self.height / 2) / self.height
        r_at_y = self.radius_bottom + (self.radius_top - self.radius_bottom) * t

        # Compute radial and vertical distances
        radial_dist = max(0, xz_dist - r_at_y)
        y_dist = max(0, abs(y) - self.height / 2)

        return np.linalg.norm([radial_dist, y_dist])

    def __repr__(self):
        return f"Cylinder(radius_top={self.radius_top}, radius_bottom={self.radius_bottom}, height={self.height}, radial_segments={self.radial_segments}, material={self.material})"