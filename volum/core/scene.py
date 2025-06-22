from volum.core.registry import ObjectRegistry
from volum.core.plugin import ScenePlugin
from volum.objects import *

from typing import List, Dict, Any, Union
import uuid, os, numpy as np


class Scene:
    def __init__(self):
        self.registry = ObjectRegistry()
        self.plugins: List[ScenePlugin] = []
        self.objects: Dict[str, Any] = {}

    def load_plugins(self, plugins: List[ScenePlugin]):
        """Load plugins into the scene's registry."""
        for plugin in plugins:
            if not isinstance(plugin, ScenePlugin):
                raise TypeError(f"Expected ScenePlugin, got {type(plugin)}")
            if plugin not in self.plugins:
                plugin.register(self.registry)
                self.plugins.append(plugin)

    def add_object(self, obj_or_type, **kwargs):
        if isinstance(obj_or_type, str):
            cls = self.registry.get_type(obj_or_type)
            if cls is None:
                raise ValueError(f"Unknown object type: {obj_or_type}")
            obj = cls(**kwargs)
        else:
            obj = obj_or_type

        # Ensure the object is a SceneObject
        if not isinstance(obj, SceneObject):
            raise TypeError(f"Object must be a SceneObject, got {type(obj)}")

        obj_id = str(len(self.objects)) or str(uuid.uuid4())
        setattr(obj, 'id', obj_id)  # set the id (SceneObject should provide an id attribute)
        self.objects[obj_id] = obj

    def serialize(self):
        return {
            "plugins": [plugin.name for plugin in self.plugins],
            "objects": [obj.to_dict() for obj in self.objects.values()]
        }

    def clear(self):
        """Clear all objects in the scene."""
        self.objects.clear()

    def save(self, path: str=os.path.join(os.getcwd(), "scene.json")):
        """Save the current scene to a JSON file."""
        import json
        with open(path, 'w') as f:
            json.dump(self.serialize(), f, indent=2)


class SceneObject:
    def __init__(self, id=None):
        self.id = id

    def to_dict(self):
        raise NotImplementedError("SceneObject subclasses must implement a to_dict() method")
    
    def distance(self, point):
        """Calculate the distance to a point in 3D space."""
        if not isinstance(point, Union[list, type(np.array), tuple]) or len(point) != 3:
            raise TypeError("Point must be a 3D coordinate (list, tuple or np.array of length 3)")

        # calculate the distance based on the object's transformation
        if isinstance(self, Transform):
            # Use the inverse transformation to get the local point
            local_point = self.inverse_transform_point(point)
            object = self.object
        else:
            local_point = point
            object = self
        
        if isinstance(object, Sphere):
            radius = object.radius
            return max(0, np.linalg.norm(local_point) - radius)
        
        elif isinstance(object, Box):
            half_extents = np.array([object.width, object.height, object.depth]) * 0.5
            clamped = np.maximum(np.abs(local_point) - half_extents, 0)
            return np.linalg.norm(clamped)
        
        elif isinstance(object, Cylinder):
            y = local_point[1]
            local_point = np.array(local_point)  # Ensure local_point is a NumPy array
            xz_dist = np.linalg.norm(local_point[[0, 2]])

            # Clamp Y to the height range
            y_clamped = np.clip(y, -object.height / 2, object.height / 2)

            # Interpolate radius at this Y height
            t = (y_clamped + object.height / 2) / object.height
            r_at_y = object.radius_bottom + (object.radius_top - object.radius_bottom) * t

            # Compute radial and vertical distances
            radial_dist = max(0, xz_dist - r_at_y)
            y_dist = max(0, abs(y) - object.height / 2)

            return np.linalg.norm([radial_dist, y_dist])

        elif isinstance(object, Plane):
            half_w = object.width / 2
            half_d = object.height / 2

            px, py, pz = local_point
            clamped_x = np.clip(px, -half_w, half_w)
            clamped_z = np.clip(pz, -half_d, half_d)

            # Closest point on the rectangle in local space
            closest = np.array([clamped_x, 0.0, clamped_z])
            dist_vector = np.array([px, py, pz]) - closest
            return np.linalg.norm(dist_vector)
        
        elif isinstance(object, Line):
            point = np.array(point)
            min_distance = float('inf')

            for i in range(len(object.points) - 1):
                A = np.array(object.points[i])
                B = np.array(object.points[i + 1])
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
        
        else:
            raise NotImplementedError(f"Distance calculation not implemented for {type(object)}")