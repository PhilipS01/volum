from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union

class SceneObjectPayload(BaseModel):
    type: str = Field(..., description="Registered object type name")
    object: Optional[Dict[str, Any]] = None
    position: Optional[List[float]] = None
    rotation: Optional[List[float]] = None
    scale: Optional[List[float]] = None
    color: Optional[Union[List[float], str]] = None
    width: Optional[float] = None
    height: Optional[float] = None
    depth: Optional[float] = None
    radius: Optional[float] = None

    class Config:
        extra = 'allow'

class ScenePayload(BaseModel):
    objects: List[SceneObjectPayload]