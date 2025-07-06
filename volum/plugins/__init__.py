from volum.plugins.base_shapes import BaseShapesPlugin
from volum.plugins.lights import LightsPlugin
from volum.plugins.volumes import VolumesPlugin
from volum.plugins.base_materials import BaseMaterialsPlugin
from volum.plugins.plotting import PlottingPlugin

__all__ = [
    "BaseShapesPlugin",
    "BaseMaterialsPlugin",
    "LightsPlugin",
    "VolumesPlugin",
    "PlottingPlugin"
]

PLUGIN_MAP = {
    "BaseShapesPlugin": BaseShapesPlugin,
    "BaseMaterialsPlugin": BaseMaterialsPlugin,
    "LightsPlugin": LightsPlugin,
    "VolumesPlugin": VolumesPlugin,
    "PlottingPlugin": PlottingPlugin
}