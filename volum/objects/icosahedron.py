import numpy as np
from typing import Optional
from volum.core.scene import SceneObject
from volum.core.materials import StandardMaterial, MeshMaterial

class Icosahedron(SceneObject):
    """Represents an icosahedron in 3D space."""
    def __init__(self, radius: float, material: Optional[MeshMaterial] = None, **kwargs):
        """Initialize an icosahedron.

        Args:
            radius (float): Radius of the icosahedron.
            material (Optional[MeshMaterial], optional): Material to use for the icosahedron. Defaults to StandardMaterial.

        Raises:
            TypeError: If the material is not a MeshMaterial.
        """

        if material is None:
            material = StandardMaterial()
            
        if not isinstance(material, MeshMaterial):
            raise TypeError(f"Icosahedron expects MeshMaterial, got {type(material)}")

        super().__init__(material, **kwargs)
        self.radius = radius

    def to_dict(self):
        return {
            "type": "Icosahedron",
            "radius": self.radius,
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        """Only using a sphere as a bounding volume for distance calculation."""
        x, y, z = point
        r = np.sqrt(x**2 + y**2 + z**2)
        return abs(r - self.radius)
    
    def __repr__(self):
        return f"Icosahedron(radius={self.radius}, material={self.material})"