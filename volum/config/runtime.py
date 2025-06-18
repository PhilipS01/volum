from pathlib import Path
from typing import Optional

class RuntimeConfig:
    def __init__(self):
        self.scene_path: Optional[Path] = None
        self.python_path: Optional[Path] = None

# Shared runtime config instance
runtime_config = RuntimeConfig()