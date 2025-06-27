import numpy as np
from typing import Union, List, Optional
from volum.core.scene import SceneObject
from volum.core.materials import LineMaterial, LineBasicMaterial, LineDashedMaterial

class Line(SceneObject):
    """Represents a polyline in space."""
    def __init__(self, *pts: Union[List, np.ndarray], material: Optional[LineMaterial]=None):
        if material is None:
            material = LineBasicMaterial()
            
        if not isinstance(material, (LineBasicMaterial, LineDashedMaterial)):
            raise TypeError(f"Line expects LineBasicMaterial or LineDashedMaterial, got {type(material)}")
        
        if len(pts) == 0:
            raise ValueError("At least one argument is required to define points.")

        if len(pts) == 1:
            # 2D array
            points = np.asarray(pts[0])
            if points.ndim != 2:
                raise ValueError("Single argument must be a 2D array-like of shape (n_points, n_dimensions).")
            if not all(len(p) == len(points[0]) for p in points):
                raise ValueError("All points in the list must have the same dimension.")
            
        else:
            # Multiple arrays (x, y, z, ...)
            arrays = [np.asarray(a) for a in pts]
            lengths = [len(a) for a in arrays]
            if not all(l == lengths[0] for l in lengths):
                raise ValueError("Coordinate arrays are not the same length.")
            points = np.stack(arrays, axis=1)

        super().__init__(material)
        self.points = points

    def __len__(self):
        """Calculate the length of the line (polyline through ordered points)."""
        total = 0.0
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]

            if not all(isinstance(coord, (int, float)) for coord in p1 + p2):
                raise ValueError("All coordinates must be numeric.")

            # Euclidean distance between p1 and p2
            dist = sum((p2[j] - p1[j]) ** 2 for j in range(len(p1))) ** 0.5
            total += dist

        return total

    def to_dict(self):
        return {
            "type": "Line",
            "args": [self.points.tolist()],
            "material": self.material.to_dict()
        }
    
    def distance_to(self, point):
        point = np.array(point)
        min_distance = float('inf')

        for i in range(len(self.points) - 1):
            A = np.array(self.points[i])
            B = np.array(self.points[i + 1])
            AB = B - A
            AP = point - A

            ab_len_squared = np.dot(AB, AB)
            if ab_len_squared == 0:
                # A and B are the same point
                dist = np.linalg.norm(AP)
            else:
                t = np.dot(AP, AB) / ab_len_squared
                t = np.clip(t, 0, 1)
                closest_point = A + t * AB
                dist = np.linalg.norm(point - closest_point)

            min_distance = min(min_distance, dist)

        return min_distance

    def __repr__(self):
        return f"Line(points={self.points}, material={self.material})"