import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial

class Torus(SceneObject):
    """Represents a torus in 3D space."""
    def __init__(self, radius: float, tube_radius: float, radial_segments: int = 16, tubular_segments: int = 48, arc: float = np.pi * 2, material: Optional[MeshMaterial] = None, **kwargs):
        """Initialize a torus.

        Args:
            radius (float): Radius of the torus.
            tube_radius (float): Radius of the torus tube.
            radial_segments (int, optional): Number of segments around the torus (default: 16).
            tubular_segments (int, optional): Number of segments along the tube (default: 48).
            arc (float, optional): The arc length of the torus (default: 2 * pi).
            material (Optional[MeshMaterial], optional): Material to use for the torus. Defaults to StandardMaterial.

        Raises:
            TypeError: If the material is not a MeshMaterial.
        """

        if material is None:
            material = StandardMaterial()
            
        if not isinstance(material, MeshMaterial):
            raise TypeError(f"Torus expects MeshMaterial, got {type(material)}")

        super().__init__(material, **kwargs)
        self.radius = radius
        self.tube_radius = tube_radius
        self.radial_segments = radial_segments
        self.tubular_segments = tubular_segments
        self.arc = arc

    def to_dict(self):
        return {
            "type": "Torus",
            "radius": self.radius,
            "tube_radius": self.tube_radius,
            "radial_segments": self.radial_segments,
            "tubular_segments": self.tubular_segments,
            "arc": self.arc,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        x, y, z = point
        q = np.array([np.sqrt(x**2 + z**2) - self.radius, y])
        return np.linalg.norm(q) - self.tube_radius

    def __repr__(self):
        return f"Torus(radius={self.radius}, tube_radius={self.tube_radius}, radial_segments={self.radial_segments}, tubular_segments={self.tubular_segments}, arc={self.arc}, material={self.material})"