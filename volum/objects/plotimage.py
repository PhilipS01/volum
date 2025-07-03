import base64, io
from matplotlib import pyplot, figure
from typing import Optional
from volum.core.scene import SceneObject

class PlotImage(SceneObject):
    """Represents a 2D plot image in the 3D scene."""
    def __init__(self, plot: figure.Figure):
        super().__init__(material=None) # PointLight does not have a material
        self.plot = plot
        self._image = None  # Placeholder for the image representation

    def to_dict(self):
        return {
            "type": "PlotImage",
            "image_data": self.plot_to_image_base64(),
            "metadata": self.plot_metadata()
        }
    
    def plot_to_image_base64(self):
        buf = io.BytesIO()
        self.plot.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return f"data:image/png;base64,{image_base64}"
    
    def plot_metadata(self):
        return {
            "axes": [
                {
                    "title": ax.get_title(),
                    "xlabel": ax.get_xlabel(),
                    "ylabel": ax.get_ylabel(),
                    "xlim": ax.get_xlim(),
                    "ylim": ax.get_ylim()
                }
                for ax in self.plot.get_axes()
            ]
        }