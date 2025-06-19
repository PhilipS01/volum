from volum.core.plugin import ScenePlugin
from volum.objects.point_light import PointLight


class LightsPlugin(ScenePlugin):
    """A plugin for adding light objects to the scene."""
    def __init__(self):
        super().__init__()
        self.name = "LightsPlugin"
        self.description = "A plugin for adding light objects to the scene."

    def register(self, registry):
        registry.register_type("PointLight", PointLight)