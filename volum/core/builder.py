from typing import Any, Dict
from .registry import ObjectRegistry


def build_object_from_dict(obj_dict: Dict[str, Any], registry: ObjectRegistry) -> Any:
    """Recursively instantiate a scene object (e.g. Box, Transform, Plot2D) from its JSON dict.
    obj_dict must contain a 'type' key.

    Args:
        obj_dict (Dict[str, Any]): The JSON-like dictionary representing the object.
        registry (ObjectRegistry): The registry of available object types.

    Raises:
        ValueError: If obj_dict is not a dict.
        ValueError: If 'type' is missing from obj_dict.
        ValueError: If the object type is not registered.

    Returns:
        Any: The instantiated scene object.
    """

    if not isinstance(obj_dict, dict):
        raise ValueError(f"Expected dict, got {type(obj_dict)}")

    obj_type = obj_dict.get("type")
    if obj_type is None:
        raise ValueError("Missing 'type' field in object definition")

    cls = registry.get_type(obj_type)
    if cls is None:
        raise ValueError(f"Unknown object type '{obj_type}'")

    # Prepare constructor kwargs
    kwargs = {}
    for attr, val in obj_dict.items():
        print(f"Processing attribute '{attr}' with value: {val}")
        if attr == "type":
            continue
        # Nested object or list of nested objects
        if isinstance(val, dict) and "type" in val:
            kwargs[attr] = build_object_from_dict(val, registry)
        else:
            kwargs[attr] = val

    # Instantiate and return
    return cls(**kwargs)
