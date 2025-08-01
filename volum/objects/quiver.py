import numpy as np
from typing import Optional, Union, List
from volum.core.scene import SceneObject
from volum.core.materials import MeshMaterial, StandardMaterial
from volum.objects.cone import Cone

class Quiver(SceneObject):
    """Represents a 2D or 3D quiver plot in the 3D scene."""

    color_schemes = ["viridis", "magma", "plasma", "inferno", "cividis"]
    colormaps = ["magnitude", "x", "y", "z"]

    def __init__(self, *args: Union[np.ndarray, List[float]], object: SceneObject = Cone(.1, .3, radial_segments=12), min_length: float = 1.0, max_length: float = 5.0, **kwargs):
        """Quiver plot constructor with flexible input handling and support for various arrow objects.
    
        Args:
            args: Point and vector component arrays.

                Can be 4 to 6 separate arrays, i.e. {X, Y, Z, U, V, W} or {X, Y, U, V}

                or one array for points and vectors respectively {[X, Y, Z], [U, V, W]}.

                Please keep in mind that the second position parameter is the "height" axis in volum.
                
                Also supports meshgrid inputs like X, Y = np.meshgrid(x, y).
            object: SceneObject to use for the arrow representation. (height will be used as the arrow length)
            colormap: Determines how colors are mapped to arrows. Options are 'magnitude' or 'height'.
            min_length: Minimum length of the arrows. (will override object's properties)
            max_length: Maximum length of the arrows. (will override object's properties)
        """

        if not isinstance(object, SceneObject):
            raise ValueError("Object must be a SceneObject")
        if not hasattr(object, 'height'):
            raise ValueError("Object must have a height property in order to be used in a Quiver")
        if not isinstance(min_length, (int, float)) or min_length <= 0:
            raise ValueError("min_length must be a positive number")
        if not isinstance(max_length, (int, float)) or max_length <= 0:
            raise ValueError("max_length must be a positive number")
        if min_length > max_length:
            raise ValueError("min_length must be less than or equal to max_length")

        assert args, "At least one argument is required for Quiver"

        # Handle input cases
        if len(args) == 6:  # [X, Y, Z, U, V, W]
            X, Y, Z, U, V, W = map(np.asarray, args)
            
            # Validate shapes
            if not (X.shape == Y.shape == Z.shape == U.shape == V.shape == W.shape):
                raise ValueError("All input arrays must have the same shape.")
            
            # Flatten arrays if they come from meshgrid
            X, Y, Z, U, V, W = map(np.ravel, (X, Y, Z, U, V, W))

            # Combine points and vectors
            pts = np.stack((X, Y, Z), axis=-1)
            vecs = np.stack((U, V, W), axis=-1)

            # Store points and vectors
            self.points = pts
            self.vectors = vecs

        elif len(args) == 2:
            shape = kwargs.get('shape', None)
            if not shape:
                self.points, self.vectors = map(np.asarray, args) # already stacked arrays (e.g. from builder)
            else: # already serialized arrays
                self.points = np.asarray(args[0]).reshape(shape)
                self.vectors = np.asarray(args[1]).reshape(shape)
            
        else:
            raise ValueError("Invalid input. Expected [X, Y, Z, U, V, W] or [[X, Y, Z], [U, V, W]].")
        
        if self.points.shape[1] > 3 or self.vectors.shape[1] > 3:
                raise ValueError("Input arrays must have shape (N, 3) or (N, 2) for points and vectors.")

        if self.points.shape[0] != self.vectors.shape[0] or self.points.shape[1] != self.vectors.shape[1]:
            raise ValueError("Points and vectors must have the same number of elements.")
        
        if isinstance(self.points, np.ndarray) and self.points.shape[1] < 3:
            # fill missing dimensions with zeros
            self.points = np.pad(self.points, ((0, 0), (0, 3 - self.points.shape[1])), mode='constant', constant_values=0)
        elif isinstance(self.points, np.ndarray) and self.points.shape[1] > 3:
            self.points = self.points[:, :3]
        
        if isinstance(self.vectors, np.ndarray) and self.vectors.shape[1] < 3:
            # fill missing dimensions with zeros
            self.vectors = np.pad(self.vectors, ((0, 0), (0, 3 - self.vectors.shape[1])), mode='constant', constant_values=0)
        elif isinstance(self.vectors, np.ndarray) and self.vectors.shape[1] > 3:
            self.vectors = self.vectors[:, :3]

        self._object = object
        # Other attributes
        self._title = kwargs.get('title', '')
        self._colormap = kwargs.get('colormap', None) if kwargs.get('colormap', None) in Quiver.colormaps else None
        self._color_scheme = kwargs.get('colorscheme', None) if kwargs.get('colorscheme', None) in Quiver.color_schemes else None
        self._min_length = min_length
        self._max_length = max_length
        self._bounds = self.points.min(axis=0).tolist() + self.points.max(axis=0).tolist()

        super().__init__(material=None, **kwargs) # No material, since the target object has it's own


    @property
    def color(self) -> str:
        """Get the color of the quiver arrows."""
        assert self.object.material, "Quiver target object must have a MeshMaterial to get color"
        return self.object.material.color
    
    @color.setter
    def color(self, value: str):
        """Set the color of the quiver arrows.
        
        Args:
            value (str): Color name, hex code or color scheme name.
        """
        if not isinstance(value, str):
            raise TypeError("color must be a string")

        assert isinstance(self.object.material, MeshMaterial), "Quiver target object must have a MeshMaterial to set color"

        self.object.material.color = value

    @property
    def colormap(self) -> Optional[str]:
        """Get the color map used for the quiver arrows."""
        return self._colormap

    @colormap.setter
    def colormap(self, value: Optional[str]):
        """Set the color map for the quiver arrows.
        Args:
            value (Optional[str]): Color map name or None.
        """
        if value not in [None, 'magnitude', 'height']:
            raise ValueError("colormap must be either 'magnitude', 'height' or None")
        self._colormap = value

    @property
    def object(self) -> SceneObject:
        """Get the SceneObject used for the arrow representation."""
        return self._object

    @object.setter
    def object(self, value: SceneObject):
        """Set the SceneObject used for the arrow representation.
        Args:
            value (SceneObject): The new SceneObject to use.
        """
        if not isinstance(value, SceneObject):
            raise TypeError("object must be a SceneObject")
        self._object = value

    @property
    def min_length(self) -> float:
        """Get the minimum length of the arrows."""
        return self._min_length
    
    @min_length.setter
    def min_length(self, value: float):
        """Set the minimum length of the arrows.
        
        Args:
            value (float): Minimum length of the arrows.
        """
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("min_length must be a positive number")
        self._min_length = value

    @property
    def max_length(self) -> float:
        """Get the maximum length of the arrows."""
        return self._max_length
    
    @max_length.setter
    def max_length(self, value: float):
        """Set the maximum length of the arrows.
        
        Args:
            value (float): Maximum length of the arrows.
        """
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("max_length must be a positive number")
        self._max_length = value

    @property
    def title(self) -> str:
        """Get the title of the quiver plot."""
        return self._title

    @title.setter
    def title(self, value: str):
        """Set the title of the quiver plot."""
        self._title = value

    def to_dict(self):
        return {
            "type": "Quiver",
            "object": self.object.to_dict(),
            "args": (self.points.flatten().tolist(), self.vectors.flatten().tolist()),
            "colormap": self.colormap,
            "colorscheme": self._color_scheme,
            "min_length": self._min_length,
            "max_length": self._max_length,
            "bounds": self._bounds,
            "shape": (self.points.shape[0], self.points.shape[1])
        }
