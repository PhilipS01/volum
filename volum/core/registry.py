class ObjectRegistry:
    """A registry for storing and retrieving object types."""
    def __init__(self):
        self.types = {}

    def register_type(self, name, cls):
        self.types[name] = cls

    def get_type(self, name):
        return self.types.get(name)
    

class RegistryWarning(Warning):
    """Base class for registry-related warnings."""
    pass

import warnings
from volum.core.materials import Material
from volum.config.constants import TerminalColors
from typing import Dict, Union, Type

class MaterialInstances:
    """A registry for storing and retrieving material instances."""
    def __init__(self):
        self.materials: Dict[str, Material] = {}

    def register_material(self, name, material):
        """Register a material instance with a name."""
        if not isinstance(material, Material):
            raise TypeError(f"Expected Material instance, got {type(material)}")
        if name in self.materials:
            warnings.warn(
                f"{TerminalColors.WARNING}Material with name '{name}' already exists in the scene. Overwriting.{TerminalColors.ENDC}",
                category=RegistryWarning,
                stacklevel=2
            )
        self.materials[name] = material

    def get_material(self, name) -> Union[Material, None]:
        return self.materials.get(name)

    def __contains__(self, name):
        return name in self.materials
    
    def clear(self):
        """Clear all registered materials."""
        self.materials.clear()

    def serialize(self):
        """Serialize the material instances to a dictionary."""
        return {name: material.to_dict() for name, material in self.materials.items()}