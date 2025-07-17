import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial

class Cone(SceneObject):
    """Represents a cone in 3D space."""
    def __init__(self, radius: float, height: float, radial_segments: int = 32, open_ended: bool = False, theta_length: float = 2*np.pi, theta_start: float = 0, material: Optional[MeshMaterial] = None, **kwargs):
        """Initialize a cone.

        Args:
            radius (float): Radius of the cone's base.
            height (float): Height of the cone.
            segments (int, optional): Number of segments for the cone's base (radial). Defaults to 32.
            open_ended (bool, optional): Determines if the cone is open-ended, i.e. if it has a base. Defaults to False.
            perimeter (float, optional): Perimeter of the cone's base. Defaults to 2*np.pi.
            perimeter_start (float, optional): Starting angle for the perimeter. Defaults to 0.
            material (Optional[MeshMaterial], optional): Material to use for the cone. Defaults to StandardMaterial.

        Raises:
            TypeError: If the material is not a MeshMaterial.
        """

        if material is None:
            material = StandardMaterial()
            
        if not isinstance(material, MeshMaterial):
            raise TypeError(f"Cone expects MeshMaterial, got {type(material)}")

        super().__init__(material, **kwargs)
        self.radius = radius
        self.height = height
        self.radial_segments = radial_segments
        self.open_ended = open_ended
        self.theta_length = theta_length
        self.theta_start = theta_start
        # Precompute some values for distance calculations
        self.slant_height = np.sqrt(radius**2 + height**2)
        self.sin_theta = radius / self.slant_height
        self.cos_theta = height / self.slant_height

    def to_dict(self):
        return {
            "type": "Cone",
            "radius": self.radius,
            "height": self.height,
            "radial_segments": self.radial_segments,
            "open_ended": self.open_ended,
            "theta_length": self.theta_length,
            "theta_start": self.theta_start,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        px, py, pz = point
        r_xz = np.sqrt(px**2 + pz**2)
        p = np.array([px, py, pz])

        # 1. Distance to lateral surface

        # Project point onto axis-aligned infinite cone
        # Represent point in (r, y) space
        q = np.array([r_xz, py])
        cone_dir = np.array([self.sin_theta, -self.cos_theta])  # outward normal of infinite cone
        signed_dist_to_cone = np.dot(q, cone_dir)

        # Closest point direction in xz-plane (radial)
        if r_xz != 0:
            radial_dir = np.array([px / r_xz, pz / r_xz])
        else:
            radial_dir = np.array([1.0, 0.0])  # arbitrary

        # Find point on the infinite cone surface in 3D
        # Let y' be the closest y along the cone's slope
        y_proj = (py - r_xz * self.radius / self.height) / (1 + (self.radius / self.height)**2)
        y_clamped = np.clip(y_proj, 0, self.height)
        r_proj = self.radius * y_clamped / self.height
        closest_lateral = np.array([
            r_proj * radial_dir[0],
            r_proj * radial_dir[1],
            y_clamped
        ])
        dist_lateral = np.linalg.norm(p - closest_lateral)

        # 2. Distance to base (disk at y = height)
        dy_base = py - self.height
        if r_xz <= self.radius:
            dist_base = abs(dy_base)
        else:
            dist_base = np.sqrt((r_xz - self.radius)**2 + dy_base**2)

        # 3. Distance to apex (optional)
        dist_apex = np.linalg.norm(p)

        # Final result
        return min(dist_lateral, dist_base, dist_apex)
    
    def __repr__(self):
        return f"Cone(radius={self.radius}, height={self.height}, radial_segments={self.radial_segments}, open_ended={self.open_ended}, theta_length={self.theta_length}, theta_start={self.theta_start}, material={self.material})"