class Serializable:
    """An interface for objects that can be serialized to a dictionary."""
    def to_dict(self):
        raise NotImplementedError
    
class Transformable:
    """An interface for objects that can be transformed."""
    def translate(self, x: float, y: float, z: float):
        raise NotImplementedError
    
    def rotate(self, angle: float, axis: str):
        raise NotImplementedError
    
    def scale(self, factor: float):
        raise NotImplementedError

class Scriptable:
    """An interface for objects that can run scripts."""
    def run_script(self, code: str):
        raise NotImplementedError
