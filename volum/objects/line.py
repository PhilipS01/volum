from numpy import ndarray
from typing import Union, List
from volum.core.scene import SceneObject

class Line(SceneObject):
    """Represents a polyline in space."""
    def __init__(self, points: Union[List, ndarray], color: str = "red"):
        super().__init__()
        if len(points) < 2:
            raise ValueError("A line must have at least two points.")
        if not all(len(p) == len(points[0]) for p in points):
            raise ValueError("All points in the list must have the same dimension.")
        if isinstance(points, list):
            if not all(isinstance(p, list) for p in points):
                raise ValueError("Points must be a 2D list (list of lists).")
        elif isinstance(points, ndarray):
            if points.ndim != 2:
                raise ValueError("Points must be a 2D numpy.ndarray.")
            points = points.tolist()
        
        self.points = points
        self.color = color

    def length(self):
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
            "points": self.points.tolist() if isinstance(self.points, ndarray) else self.points,
            "color": self.color
        }
