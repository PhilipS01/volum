import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial

class Ring(SceneObject):
    """Represents a ring in 3D space."""
    def __init__(self, inner_radius: float, outer_radius: float, segments: int = 32, perimeter: float = 2*np.pi, perimeter_start: float = 0, material: Optional[MeshMaterial] = None, **kwargs):
        """Initialize a ring.

        Args:
            inner_radius (float): Inner radius of the ring.
            outer_radius (float): Outer radius of the ring.
            segments (int, optional): Number of segments for the ring. Defaults to 32.
            perimeter (float, optional): Perimeter of the ring. Defaults to 2*pi.
            perimeter_start (float, optional): Starting angle for the perimeter. Defaults to 0.
            material (Optional[MeshMaterial], optional): Material to use for the ring. Defaults to StandardMaterial.

        Raises:
            TypeError: If the material is not a MeshMaterial.
        """
        if material is None:
            material = StandardMaterial()
            
        if not isinstance(material, MeshMaterial):
            raise TypeError(f"Ring expects MeshMaterial, got {type(material)}")

        super().__init__(material, **kwargs)
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.segments = segments
        self.perimeter = perimeter
        self.perimeter_start = perimeter_start

    def to_dict(self):
        return {
            "type": "Ring",
            "inner_radius": self.inner_radius,
            "outer_radius": self.outer_radius,
            "theta_segments": self.segments,
            "theta_length": self.perimeter,
            "theta_start": self.perimeter_start,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        px, py, pz = point
        r = np.sqrt(px**2 + pz**2)

        if self.inner_radius <= r <= self.outer_radius:
            # Point is above or below the ring
            return abs(py)
        elif r < self.inner_radius:
            # Closest point is on the inner edge
            closest_r = self.inner_radius
        else:
            # Closest point is on the outer edge
            closest_r = self.outer_radius

        # Closest point on ring's edge in XZ plane
        if r == 0:
            # Arbitrary direction when point is at origin
            closest_xz = np.array([closest_r, 0, 0])
        else:
            closest_xz = np.array([px, 0, pz]) * (closest_r / r)

        closest_point = np.array([closest_xz[0], 0, closest_xz[2]])
        point_vec = np.array([px, py, pz])
        return np.linalg.norm(point_vec - closest_point)
    
    def __repr__(self):
        return f"Ring(inner_radius={self.inner_radius}, outer_radius={self.outer_radius}, segments={self.segments}, perimeter={self.perimeter}, perimeter_start={self.perimeter_start}, material={self.material})"