import numpy as np
from volum.core.scene import SceneObject


class Plane(SceneObject):
    """Represents a plane in 3D space defined by a point and a normal vector."""
    def __init__(self, width:float , height: float, color: str = 'gray'):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color

    def to_dict(self):
        return {
            "type": "Plane",
            "width": self.width,
            "height": self.height,
            "color": self.color
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
        return f"Plane(width={self.width}, height={self.height}, color={self.color})"