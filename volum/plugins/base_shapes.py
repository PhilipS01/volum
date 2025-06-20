from volum.core.plugin import ScenePlugin

from volum.objects.box import Box
from volum.objects.sphere import Sphere
from volum.objects.plane import Plane
from volum.objects.transform import Transform
from volum.objects.cylinder import Cylinder
from volum.objects.line import Line


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
