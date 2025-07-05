import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial

class TorusKnot(SceneObject):
    """Represents a torus knot in 3D space."""
    def __init__(self, radius: float, tube_radius: float, tubular_segments: int = 64, radial_segments: int = 16, p: int = 2, q: int = 3, material: Optional[MeshMaterial] = None, **kwargs):
        """Initialize a torus knot.

        Args:
            radius (float): Radius of the torus.
            tube_radius (float): Radius of the torus tube.
            radial_segments (int, optional): Number of segments around the torus (default: 16).
            tubular_segments (int, optional): Number of segments along the tube (default: 64).
            p (int, optional): How many times the geometry winds around its axis of rotational symmetry (default: 2).
            q (int, optional): How many times the geometry winds around a circle in the interior of the torus (default: 3).
            material (Optional[MeshMaterial], optional): Material to use for the torus. Defaults to StandardMaterial.

        Raises:
            TypeError: If the material is not a MeshMaterial.
        """

        if material is None:
            material = StandardMaterial()
            
        if not isinstance(material, MeshMaterial):
            raise TypeError(f"TorusKnot expects MeshMaterial, got {type(material)}")

        super().__init__(material, **kwargs)
        self.radius = radius
        self.tube_radius = tube_radius
        self.radial_segments = radial_segments
        self.tubular_segments = tubular_segments
        self.p = p
        self.q = q

    def to_dict(self):
        return {
            "type": "TorusKnot",
            "radius": self.radius,
            "tube_radius": self.tube_radius,
            "radial_segments": self.radial_segments,
            "tubular_segments": self.tubular_segments,
            "p": self.p,
            "q": self.q,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        t_vals = np.linspace(0, 2 * np.pi, 500)
        min_dist = float('inf')
        point = np.array(point)

        for t in t_vals:
            knot_pt = self._torus_knot_point(t, self.p, self.q, self.radius, self.tube_radius)
            dist = np.linalg.norm(point - knot_pt)
            if dist < min_dist:
                min_dist = dist

        return min_dist
    
    def _torus_knot_point(self, t, p, q, R, r):
        x = (R + r * np.cos(q * t)) * np.cos(p * t)
        y = (R + r * np.cos(q * t)) * np.sin(p * t)
        z = r * np.sin(q * t)
        return np.array([x, y, z])

    def __repr__(self):
        return f"TorusKnot(radius={self.radius}, tube_radius={self.tube_radius}, radial_segments={self.radial_segments}, tubular_segments={self.tubular_segments}, p={self.p}, q={self.q})"