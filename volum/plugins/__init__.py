from volum.plugins.base_shapes import BaseShapesPlugin
from volum.plugins.lights import LightsPlugin
from volum.plugins.volumes import VolumesPlugin
from volum.plugins.base_materials import BaseMaterialsPlugin

__all__ = [
    "BaseShapesPlugin",
    "BaseMaterialsPlugin",
    "LightsPlugin",
    "VolumesPlugin"
]

PLUGIN_MAP = {
    "BaseShapesPlugin": BaseShapesPlugin,
    "BaseMaterialsPlugin": BaseMaterialsPlugin,
    "LightsPlugin": LightsPlugin,
    "VolumesPlugin": VolumesPlugin,
}