from volum.core.scene import SceneObject

class Transform(SceneObject):
    """Represents a transformation applied to a SceneObject, including position, rotation, and scale."""
    def __init__(self, object: SceneObject, position=None, rotation=None, scale=None):
        
        if not isinstance(object, SceneObject):
            raise TypeError(f"{object} is not a SceneObject.")
        
        super().__init__()
        self.object = object
        self.position = position or [0, 0, 0]
        self.rotation = rotation or [0, 0, 0]
        self.scale = scale or [1, 1, 1]

    def to_dict(self):
        return {
            "type": "Transform",
            "position": self.position,
            "rotation": self.rotation,
            "scale": self.scale,
            "object": self.object.to_dict()
        }

    def inverse_transform_point(self, point):
        """Apply the inverse transformation to a point in 3D space."""
        import numpy as np

        def rotation_matrix_from_euler(rx, ry, rz):
            # Basic Euler XYZ rotation matrices
            cx, sx = np.cos(rx), np.sin(rx)
            cy, sy = np.cos(ry), np.sin(ry)
            cz, sz = np.cos(rz), np.sin(rz)

            Rx = np.array([
                [1, 0, 0],
                [0, cx, -sx],
                [0, sx, cx]
            ])

            Ry = np.array([
                [cy, 0, sy],
                [0, 1, 0],
                [-sy, 0, cy]
            ])

            Rz = np.array([
                [cz, -sz, 0],
                [sz, cz, 0],
                [0, 0, 1]
            ])

            # Apply rotations in ZYX order (common in graphics)
            return Rz @ Ry @ Rx
    
        def inverse_rotation_matrix(euler):
            rx, ry, rz = euler
            # Inverse rotation is R(-z) @ R(-y) @ R(-x)
            return rotation_matrix_from_euler(-rx, -ry, -rz)


        point = np.array(point)
        pos = np.array(self.position)
        rot = np.array(self.rotation)
        scale = np.array(self.scale)
        if len(point) != 3 or len(pos) != 3 or len(rot) != 3 or len(scale) != 3:
            raise ValueError("Point, position, rotation, and scale must be 3D vectors.")
        # Remove translation
        local_point = point - pos
    
        # Inverse rotation
        R_inv = inverse_rotation_matrix(rot)
        local_point = R_inv @ local_point
    
        # Inverse scale
        with np.errstate(divide='ignore', invalid='ignore'):
            local_point = np.divide(local_point, scale, out=np.zeros_like(local_point), where=scale!=0)
    
        return local_point
    
    