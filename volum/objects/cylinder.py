from volum.core.scene import SceneObject

class Cylinder(SceneObject):
    """Represents a cylinder object in the scene."""
    def __init__(self, radius_top: float, radius_bottom: float, height: float, color: str = "gray", radial_segments: int = 64):
        super().__init__()
        self.radius_top = radius_top
        self.radius_bottom = radius_bottom
        self.height = height
        self.color = color
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
            "color": self.color,
            "radial_segments": self.radial_segments
        }

    def __repr__(self):
        return f"Cylinder(radius_top={self.radius_top}, radius_bottom={self.radius_bottom}, height={self.height}, color={self.color}, radial_segments={self.radial_segments})"