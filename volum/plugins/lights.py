from volum.core.plugin import ScenePlugin
from volum.objects.point_light import PointLight


class LightsPlugin(ScenePlugin):
    """A plugin for adding light objects to the scene."""
    name = "LightsPlugin"
    description = "A plugin for adding light objects to the scene."

    def register(self, registry):
        registry.register_type("PointLight", PointLight)