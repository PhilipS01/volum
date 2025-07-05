import base64, io
from matplotlib import figure
from typing import Optional
from volum.core.scene import SceneObject

class PlotImage(SceneObject):
    """Represents a 2D plot image in the 3D scene."""
    _figure_cache = {}

    def __new__(cls, plot: Optional[figure.Figure] = None, **kwargs):
        # Check if this figure is already in cache, reuse if so
        if plot and plot.number in cls._figure_cache: # type: ignore
            return cls._figure_cache[plot.number] # type: ignore
        
        instance = super().__new__(cls)
        return instance

    def __init__(self, plot: figure.Figure, width: int = 5, height: int = 4, double_sided: bool = False):
        """Initialize the PlotImage.

        Args:
            plot (figure.Figure): The matplotlib figure to be used as the plot.
            width (int, optional): The width of the plot image. Defaults to 5.
            height (int, optional): The height of the plot image. Defaults to 4.
            double_sided (bool, optional): Whether the plot image is double-sided. Defaults to False.
        """

        super().__init__(material=None) # PlotImage does not have a material
        self.plot = plot
        self._image = None  # placeholder
        self.width = width
        self.height = height
        self.double_sided = double_sided

        # cache this instance
        if plot and hasattr(plot, "number"):
            self._figure_cache[plot.number] = self # type: ignore
    
    @property
    def image(self) -> Optional[str]:
        """Get the image representation of the plot."""
        if self._image is None:
            self._image = self.plot_to_image_base64()
        return self._image

    @classmethod
    def from_dict(cls, data: dict) -> "PlotImage":
        import matplotlib
        matplotlib.use('Agg')  # Use non-GUI backend before importing pyplot
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots()

        x_data = data.get("x", [])
        y_data = data.get("y", [])
        for x, y in zip(x_data, y_data):
            ax.plot(x, y)

        meta = data.get("metadata", {}).get("axes", [{}])[0]
        ax.set_title(meta.get("title", ""))
        ax.set_xlabel(meta.get("xlabel", ""))
        ax.set_ylabel(meta.get("ylabel", ""))
        if "xlim" in meta:
            ax.set_xlim(meta["xlim"])
        if "ylim" in meta:
            ax.set_ylim(meta["ylim"])

        return cls(plot=fig, width=data.get("width", 5), height=data.get("height", 4), double_sided=data.get("double_sided", False))

    def to_dict(self):
        x_data = []
        y_data = []
        
        ax = self.plot.get_axes()[0] # assuming a single axis for simplicity
        if ax:
            lines = ax.get_lines()
            if lines:
                x_data = [line.get_xdata().tolist() for line in lines] # type: ignore
                y_data = [line.get_ydata().tolist() for line in lines] # type: ignore

        return {
            "type": "PlotImage",
            "image_data": self.image,
            "x": x_data,
            "y": y_data,
            "metadata": self.plot_metadata(),
            "width": self.width,
            "height": self.height,
            "double_sided": self.double_sided
        }
    
    def plot_to_image_base64(self):
        # Ensure plot has same aspect ratio as specified width and height
        self.plot.set_size_inches(self.width, self.height, forward=True)
        # Convert the plot to a PNG image in base64 format
        buf = io.BytesIO()
        self.plot.savefig(buf, format='png', bbox_inches='tight', dpi=300)
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
                    "ylim": ax.get_ylim(),
                    "legend": True,
                    "label": "Sample Line"
                }
                for ax in self.plot.get_axes()
            ]
        }
