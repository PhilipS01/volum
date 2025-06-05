from core.interfaces import Serializable

class Sphere(Serializable):
    def __init__(self, radius, color: str = "gray"):
        self.radius = radius
        self.color = color

    def volume(self):
        return (4/3) * 3.14159 * (self.radius ** 3)

    def surface_area(self):
        return 4 * 3.14159 * (self.radius ** 2)

    def to_dict(self):
        return {
            "type": "Sphere",
            "radius": self.radius,
            "color": self.color
        }