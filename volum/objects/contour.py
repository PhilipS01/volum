import numpy as np
from typing import Optional, Union, List
from volum.core.scene import SceneObject
from volum.core.materials import BasicMaterial, MeshMaterial
from volum.objects.cone import Cone

class Contour(SceneObject):
    """Represents a 2D or 3D contour plot in the 3D scene."""

    color_schemes = ["viridis", "magma", "plasma", "inferno", "cividis"]
    colormaps = ["x", "y", "z"]

    def __init__(self, *args: Union[np.typing.NDArray[np.float64], List[float]], material: MeshMaterial = BasicMaterial(), **kwargs):
        """Contour plot constructor with flexible input handling.

        Args:
            args: Arrays representing sample points from which the surface will be reconstructed.
                
                Can be 2 to 3 separate arrays, i.e. {X, Y, Z, W} or {X, Y, Z=W}

                Please keep in mind that the second position parameter is the "height" axis in volum.
                
                Also supports meshgrid inputs like X, Y = np.meshgrid(x, y).
            object: SceneObject to use for the arrow representation. (height will be used as the arrow length)
            colormap: Determines how colors are mapped to arrows. Options are 'magnitude' or 'height'.
            min_length: Minimum length of the arrows. (will override object's properties)
            max_length: Maximum length of the arrows. (will override object's properties)
        """

        assert args, "At least one argument is required for Contour"
        self.shape = kwargs.get('shape', None)

        # Handle input cases
        if len(args) == 4:  # [X, Y, Z, W]
            X, Y, Z, W = map(np.asarray, args)

            # Validate shapes
            if not X.shape == Y.shape == Z.shape:
                raise ValueError("All points in the array must have the same shape.")
            
            if not W.shape[1] == 1:
                raise ValueError("W must be a 1D array representing scalar values.")
            
            if not len(W) == len(X) == len(Y) == len(Z):
                raise ValueError("X, Y, Z and W must have the same length.")
            
            # Flatten arrays if they come from meshgrid
            X, Y, Z = map(np.ravel, (X, Y, Z))

            # Combine points and vectors
            pts = np.stack((X, Y, Z), axis=-1)

            # Store points and vectors
            self.points = pts
            self.values = W
            self.shape = (int((len(X))**(1/3)+1), int((len(Y))**(1/3)+1), int((len(Z))**(1/3)+1)) if self.shape is None else self.shape

        elif len(args) == 3:  # [X, Y, Z=W]
            ...
        
        elif len(args) == 2:  # single stream of points (e.g. once serialized)
            if not self.shape:
                self.points, self.values = map(np.asarray, args)
            else:
                self.points = np.asarray(args[0])
                self.values = np.asarray(args[1])

        else:
            raise ValueError("Invalid input. Expected [X, Y, Z, U, V, W] or [[X, Y, Z], [U, V, W]].")
        

        if material is not None and not isinstance(material, MeshMaterial):
            raise TypeError(f"Contour expects MeshMaterial, got {type(material)}")

        # Other attributes
        self._title = kwargs.get('title', '')
        self._colormap = kwargs.get('colormap', None) if kwargs.get('colormap', None) in Contour.colormaps else None
        self._color_scheme = kwargs.get('colorscheme', None) if kwargs.get('colorscheme', None) in Contour.color_schemes else None
        self._bounds = self.points.min(axis=0).tolist() + self.points.max(axis=0).tolist() if kwargs.get('bounds', None) is None else kwargs['bounds']

        super().__init__(material=material, **kwargs) # No material, since the target object has it's own


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
    def title(self) -> str:
        """Get the title of the quiver plot."""
        return self._title

    @title.setter
    def title(self, value: str):
        """Set the title of the quiver plot."""
        self._title = value

    def to_dict(self):
        values = self.values.reshape(self.shape).astype(np.float32).flatten(order='C').tolist() if len(self.values) != len(self.points)*3 else self.values.flatten(order='C').tolist()
        return {
            "type": "Contour",
            "material": self.material.to_dict() if self.material else None,
            "args": (self.points.flatten().tolist(), values), # row-major (x-fastest) order for the values, to enable direct use in JS DataTexture
            "colormap": self.colormap,
            "colorscheme": self._color_scheme,
            "bounds": list(self._bounds),
            "shape": self.shape
        }
