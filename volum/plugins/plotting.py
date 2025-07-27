from volum.core.plugin import ScenePlugin

from volum.objects import PlotImage
from volum.objects import Quiver
from volum.objects import Contour


class PlottingPlugin(ScenePlugin):
    """A plugin for adding basic geometric shapes to the scene."""
    name = "PlottingPlugin"
    description = "A plugin for adding plotting capabilities to the scene."

    def register(self, registry):
        registry.register_type("PlotImage", PlotImage)
        registry.register_type("Quiver", Quiver)
        registry.register_type("Contour", Contour)
