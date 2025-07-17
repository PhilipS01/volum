import numpy as np
from typing import Optional, Union, List
from volum.core.scene import SceneObject
from volum.core.materials import MeshMaterial, StandardMaterial
from volum.objects.cone import Cone

class Quiver(SceneObject):
    """Represents a 2D or 3D quiver plot in the 3D scene."""

    _color: str = 'black'  # Default color for the arrows


    def __init__(self, *comps: Union[np.typing.NDArray[np.float64], List[float]], object: SceneObject = Cone(1,3, 3), material: Union[MeshMaterial, str, None], colormap: Optional[str], **kwargs):
        """Initialize the Quiver.

        Args:
            comps: Arrays representing points and vector components.
                
                Can be [X, Y, Z, U, V, W] or [X, Y, Z], [U, V, W].
                
                X, Y, Z, U, V, W can be arrays of floats.
                
                Also supports meshgrid inputs like X, Y = np.meshgrid(x, y).
            object: SceneObject to use for the arrow representation.
            material: Material for the arrow objects. Set it's color attribute to color scheme like 'viridis' or 'plasma' if using a colormap.
            colormap: Determines how colors are mapped to arrows. 
                Options are 'magnitude' or 'height'.
        """

        if material is None:
            material = StandardMaterial()

        assert isinstance(object, SceneObject), "Object must be a SceneObject"
        assert isinstance(material, (MeshMaterial, str)), "Material must be a MeshMaterial or a string"
        assert colormap in [None, 'magnitude', 'height'], "colormap must be either 'magnitude' or 'height' or None"

        # Handle input cases
        if len(comps) == 6:  # [X, Y, Z, U, V, W]
            X, Y, Z, U, V, W = map(np.asarray, comps)
        elif len(comps) == 2:  # [X, Y, Z], [U, V, W]
            pts, vecs = map(np.asarray, comps)
            if pts.shape[0] != 3 or vecs.shape[0] != 3:
                raise ValueError("Expected [X, Y, Z], [U, V, W] with each being arrays of floats.")
            X, Y, Z = pts
            U, V, W = vecs
        else:
            raise ValueError("Invalid input. Expected [X, Y, Z, U, V, W] or [X, Y, Z], [U, V, W].")

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
        self._object = object
        # Other attributes
        self._title = kwargs.pop('title', '')
        self._colormap = colormap

        super().__init__(material=material, **kwargs)


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

    #@classmethod
    #def from_dict(cls, data: dict) -> "Quiver":
    #    import matplotlib
    #    matplotlib.use('Agg')  # Use non-GUI backend before importing pyplot
    #    import matplotlib.pyplot as plt
    #    
    #    fig, ax = plt.subplots()
    #
    #    x_data = data.get("x", [])
    #    y_data = data.get("y", [])
    #    for x, y in zip(x_data, y_data):
    #        ax.plot(x, y)
    #
    #    meta = data.get("metadata", {}).get("axes", [{}])[0]
    #    ax.set_title(meta.get("title", ""))
    #    ax.set_xlabel(meta.get("xlabel", ""))
    #    ax.set_ylabel(meta.get("ylabel", ""))
    #    if "xlim" in meta:
    #        ax.set_xlim(meta["xlim"])
    #    if "ylim" in meta:
    #        ax.set_ylim(meta["ylim"])
    #
    #    return cls(plot=fig, width=data.get("width", 5), height=data.get("height", 4), double_sided=data.get("double_sided", False))

    def to_dict(self):
        

        return {
            "type": "Quiver",
            "object": self.object.to_dict(),
            "material": self.material.to_dict(),
            "points": self.points.tolist(),
            "vectors": self.vectors.tolist(),
            "colormap": self.colormap,
        }
