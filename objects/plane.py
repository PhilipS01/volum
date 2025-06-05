from core.interfaces import Serializable

class Plane(Serializable):
    def __init__(self, position, normal):
        self.position = position  # A point on the plane
        self.normal = normal      # A vector normal to the plane

    def is_point_on_plane(self, point):
        """Check if a point is on the plane."""
        return abs((point - self.position).dot(self.normal)) < 1e-6

    def to_dict(self):
        return {
            "type": "Plane",
            "position": self.position,
            "normal": self.normal
        }