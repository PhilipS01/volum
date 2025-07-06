from volum.core.plugin import ScenePlugin

from volum.core.materials import StandardMaterial, BasicMaterial, PhongMaterial, LineBasicMaterial, LineDashedMaterial, PhysicalMaterial, MatcapMaterial, NormalMaterial, ToonMaterial, ImageMaterial

class BaseMaterialsPlugin(ScenePlugin):
    """A plugin for adding basic materials to the scene."""
    name = "BaseMaterialsPlugin"
    description = "A plugin for adding basic materials to the scene."
        
    def register(self, registry):
        registry.register_type("StandardMaterial", StandardMaterial)
        registry.register_type("BasicMaterial", BasicMaterial)
        registry.register_type("PhongMaterial", PhongMaterial)
        registry.register_type("LineBasicMaterial", LineBasicMaterial)
        registry.register_type("LineDashedMaterial", LineDashedMaterial)
        registry.register_type("PhysicalMaterial", PhysicalMaterial)
        registry.register_type("MatcapMaterial", MatcapMaterial)
        registry.register_type("NormalMaterial", NormalMaterial)
        registry.register_type("ToonMaterial", ToonMaterial)
        registry.register_type("ImageMaterial", ImageMaterial)
