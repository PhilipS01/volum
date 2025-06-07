class ScenePlugin:
    """Basic plugin for adding objects to the scene."""
    def register(self, registry):
        raise NotImplementedError("Plugins must implement the register() method")
