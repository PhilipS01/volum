from volum.core.plugin import ScenePlugin

from volum.core.materials import StandardMaterial, BasicMaterial, LineBasicMaterial, LineDashedMaterial

class BaseMaterialsPlugin(ScenePlugin):
    """A plugin for adding basic materials to the scene."""
    name = "BaseMaterialsPlugin"
    description = "A plugin for adding basic materials to the scene."
        
    def register(self, registry):
        registry.register_type("StandardMaterial", StandardMaterial)
        registry.register_type("BasicMaterial", BasicMaterial)
        registry.register_type("LineBasicMaterial", LineBasicMaterial)
        registry.register_type("LineDashedMaterial", LineDashedMaterial)
