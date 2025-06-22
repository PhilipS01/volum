class Serializable:
    """An interface for objects that can be serialized to a dictionary."""
    def to_dict(self):
        raise NotImplementedError("Object extends Serializable and must therefore implement to_dict() method")

class Scriptable:
    """An interface for objects that can run scripts."""
    def run_script(self, code: str):
        raise NotImplementedError("Object extends Scriptable and must therefore implement run_script() method")
