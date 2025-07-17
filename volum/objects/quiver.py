import numpy as np
from typing import Optional, Union, List
from volum.core.scene import SceneObject
from volum.core.materials import MeshMaterial, StandardMaterial
from volum.objects.cone import Cone

class Quiver(SceneObject):
    """Represents a 2D or 3D quiver plot in the 3D scene."""

    color_schemes = ["viridis", "magma", "plasma", "inferno", "cividis"]

    def __init__(self, *args: Union[np.typing.NDArray[np.float64], List[float]], object: SceneObject = Cone(.1, .3, radial_segments=12), colormap: Optional[str] = None, **kwargs):
        """Initialize the Quiver.
    
        Args:
            comps: Arrays representing points and vector components.
                
                Can be [X, Y, Z, U, V, W] or [X, Y, Z], [U, V, W].
                
                X, Y, Z, U, V, W can be arrays of floats.

                Please keep in mind that the second position parameter is the "height" axis in volum.
                
                Also supports meshgrid inputs like X, Y = np.meshgrid(x, y).
            object: SceneObject to use for the arrow representation.
            material: Material for the arrow objects. Set it's color attribute to color scheme like 'viridis' or 'magma' if using a colormap.
            colormap: Determines how colors are mapped to arrows. 
                Options are 'magnitude' or 'height'.
        """

        assert isinstance(object, SceneObject), "Object must be a SceneObject"
        assert colormap in [None, 'magnitude', 'height'], "colormap must be either 'magnitude' or 'height' or None"

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

        elif len(args) == 2:  # already stacked arrays (e.g. from builder)
            self.points, self.vectors = map(np.asarray, args)

            if self.points.shape[1] != 3 or self.vectors.shape[1] != 3:
                raise ValueError("Input arrays must have shape (3, N) for points and vectors.")
            
        else:
            raise ValueError("Invalid input. Expected [X, Y, Z, U, V, W] or [[X, Y, Z], [U, V, W]].")

       
        self._object = object
        # Other attributes
        self._title = kwargs.pop('title', '')
        self._colormap = colormap
        self._color = kwargs.pop('color', None)

        super().__init__(material=None, **kwargs)


    @property
    def color(self) -> str:
        """Get the color of the quiver arrows."""
        return self._color
    
    @color.setter
    def color(self, value: str):
        """Set the color of the quiver arrows.
        
        Args:
            value (str): Color name, hex code or color scheme name.
        """
        if not isinstance(value, str):
            raise TypeError("color must be a string")

        assert isinstance(self.object.material, MeshMaterial), "Quiver target object must have a MeshMaterial"

        if value not in Quiver.color_schemes:
            self.object.material.color = value

        self._color = value

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
            "args": (self.points.tolist(), self.vectors.tolist()),
            "colormap": self.colormap,
            "colorscheme": self.color if self.color in Quiver.color_schemes else None,
        }
