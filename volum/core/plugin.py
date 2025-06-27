class ScenePlugin:
    """Basic plugin to allow scene manipulation."""
    name="ScenePlugin"
        
    def register(self, registry):
        raise NotImplementedError("Plugins must implement the register() method")
