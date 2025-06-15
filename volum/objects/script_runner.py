from ..core.interfaces import Scriptable

class ScriptRunner:
    """A class that runs scripts on scriptable objects."""
    def __init__(self, target: Scriptable, code: str):
        if not isinstance(target, Scriptable):
            raise TypeError(f"{target} is not scriptable.")
        self.target = target
        self.code = code

    def run(self):
        self.target.run_script(self.code)