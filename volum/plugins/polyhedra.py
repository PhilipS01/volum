from volum.core.plugin import ScenePlugin

from volum.objects import Tetrahedron
from volum.objects import Dodecahedron
from volum.objects import Icosahedron
from volum.objects import Octahedron


class PolyhedraPlugin(ScenePlugin):
    """A plugin for adding polyhedral shapes to the scene."""
    name = "PolyhedraPlugin"
    description = "A plugin for adding polyhedral shapes to the scene."

    def register(self, registry):
        registry.register_type("Tetrahedron", Tetrahedron)
        registry.register_type("Dodecahedron", Dodecahedron)
        registry.register_type("Icosahedron", Icosahedron)
        registry.register_type("Octahedron", Octahedron)
