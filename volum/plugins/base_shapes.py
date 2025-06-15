from ..core.plugin import ScenePlugin
from ..objects.box import Box
from ..objects.sphere import Sphere
from ..objects.plane import Plane
from ..objects.transform import Transform
from ..objects.cylinder import Cylinder
from ..objects.line import Line


class BaseShapesPlugin(ScenePlugin):
    """A plugin for adding basic geometric shapes to the scene."""
    def register(self, registry):
        registry.register_type("Box", Box)
        registry.register_type("Sphere", Sphere)
        registry.register_type("Plane", Plane)
        registry.register_type("Transform", Transform)
        registry.register_type("Cylinder", Cylinder)
        registry.register_type("Line", Line)
