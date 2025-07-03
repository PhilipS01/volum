from volum.core.plugin import ScenePlugin

from volum.objects import Box
from volum.objects import Sphere
from volum.objects import Plane
from volum.objects import Transform
from volum.objects import Cylinder
from volum.objects import Line
from volum.objects import Capsule
from volum.objects import Cone
from volum.objects import Circle
from volum.objects import Ring
from volum.objects import PlotImage
from volum.objects import Torus
from volum.objects import TorusKnot


class BaseShapesPlugin(ScenePlugin):
    """A plugin for adding basic geometric shapes to the scene."""
    name = "BaseShapesPlugin"
    description = "A plugin for adding basic geometric shapes to the scene."
        
    def register(self, registry):
        registry.register_type("Box", Box)
        registry.register_type("Sphere", Sphere)
        registry.register_type("Plane", Plane)
        registry.register_type("Transform", Transform)
        registry.register_type("Cylinder", Cylinder)
        registry.register_type("Line", Line)
        registry.register_type("Capsule", Capsule)
        registry.register_type("Cone", Cone)
        registry.register_type("Circle", Circle)
        registry.register_type("Ring", Ring)
        registry.register_type("Torus", Torus)
        registry.register_type("TorusKnot", TorusKnot)
        registry.register_type("PlotImage", PlotImage)
