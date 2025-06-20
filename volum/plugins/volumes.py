from volum.core.plugin import ScenePlugin
from volum.objects.volume import Volume

class VolumesPlugin(ScenePlugin):
    """A plugin for adding volume objects to the scene."""
    name = "VolumesPlugin"
    description = "A plugin for adding volume objects to the scene."
    
    def register(self, registry):
        registry.register_type("Volume", Volume)