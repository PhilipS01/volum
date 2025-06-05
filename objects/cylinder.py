from core.interfaces import Serializable

class Cylinder(Serializable):
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height

    def volume(self):
        from math import pi
        return pi * (self.radius ** 2) * self.height

    def surface_area(self):
        from math import pi
        return 2 * pi * self.radius * (self.radius + self.height)

    def to_dict(self):
        return {
            "type": "Cylinder",
            "radius": self.radius,
            "height": self.height
        }
    
    def __repr__(self):
        return f"Cylinder(radius={self.radius}, height={self.height})"