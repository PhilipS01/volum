from volum.core.scene import SceneObject

class Volume(SceneObject):
    """Represents a 3D volume object via a file path."""
    def __init__(self, width: float, height: float, depth: float, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.width = width
        self.height = height
        self.depth = depth

    def __repr__(self):
        return f"Volume(file_path={self.file_path}, width={self.width}, height={self.height}, depth={self.depth})"

    def to_dict(self):
        return {
            "type": "Volume",
            "file_path": self.file_path,
            "width": self.width,
            "height": self.height,
            "depth": self.depth,
        }
