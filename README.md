[![Header](https://github.com/PhilipS01/volum/blob/90af00489989d70374ed29e45c32f310740daca2/docs/static/volum_banner.png)](https://volumeditor.tech/)

[**Volum**](https://volumeditor.tech/) is a modular, extensible Python toolkit for building and rendering interactive 3D scenes that can integrate data visualizations, plots, and geometry — all programmable from Python.

Python has long been the go-to language for data scientists and hobbyists to visualize data in static, two-dimensional formats. Volum transforms this experience by enabling true 3D visualization—making it easy to convert and explore your 2D data in immersive, three-dimensional environments. Because it's **plugins** from the ground up, it makes extending functionality a breeze.

## ✨ Features
- Define 3D scenes programmatically in Python
- **Scriptable** objects (e.g., dynamic data plots, script runner)
- Built-in objects like Box, Sphere, Plane, Plot2D, and Plot3D
- Transform objects (position, rotation, scale) with a clean API
- Plugin architecture to add new object types or behaviors
- Scene serialization to JSON for use in a viewer
- JavaScript scene loader takes scenes and builds them in the browser
- Renders via [Three.js](https://github.com/mrdoob/three.js), with support for more WebGL frameworks coming
- RESTful interface to sync scene state to a browser

## 📦 Installation

Coming soon ...

## 🚀 Quick Example

```python
from volum import Scene
from plugins.base_shapes import BaseShapesPlugin
from plugins.data_plots import DataPlotsPlugin
from objects import Box, Plot2D, Transform

scene = Scene()
scene.load_plugins([BaseShapesPlugin(), DataPlotsPlugin()])

box = Transform(
    object=Box(width=1, height=1, depth=1, color='green'),
    position=[1, 0, 0],
    rotation=[0, 45, 0]
)

# Rotate a 2D plot to face the camera
plot = Transform(
    object=Plot2D(data=[[1,2,3],[3,2,1]]),
    position=[0, 1, 0],
    scale=[2, 2, 2]
)

scene.add_object(box)
scene.add_object(plot)

print(scene.serialize())  # outputs scene as JSON
```

## 🔌 Plugin System
The plugin system allows developers to extend Volum by adding new object types, behaviors, or utilities without modifying the core library. Each plugin is a Python class that inherits from the ScenePlugin interface and registers new functionality with the internal object registry.

### How It Works:
1. Define a new scene object (e.g., a custom geometry or data visualization)
2. Implement the object class, including a `to_dict()` method
3. Create a plugin class that inherits from `ScenePlugin`
4. Register the object inside the plugin's `register()` method

### Plugin Example:
```python
from volum import ScenePlugin
from my_shapes.pyramid import Pyramid

class PyramidPlugin(ScenePlugin):
    def register(self, registry):
        registry.register_type("Pyramid", Pyramid)
```

### Load the Plugin:
```python
from volum import Scene
from my_shapes.plugin import PyramidPlugin

scene = Scene()
scene.load_plugins([PyramidPlugin()])
scene.add_object("Pyramid", base=2, height=3, color="gold")

print(scene.serialize())
```

### Plugin Capabilities:
- New object types (with render and serialization logic)
- Scriptable elements for dynamic behavior
- Scene modifiers (e.g. animations, transformations)
- Custom REST/API integrations or visual widgets (planned)

Plugins can be organized in separate files or even distributed as standalone Python packages for reuse and sharing.

## 🧠 Object Model
Each scene object must implement a `to_dict()` method for serialization. Optional interfaces include:
- `Serializable` – provides `to_dict()`
- `Scriptable` – supports dynamic Python scripting (e.g., `run_script(code)`)

## 📁 Project Structure
```
volum/
├── core/            # Scene engine, registry, plugin system
├── objects/         # Built-in object definitions
├── plugins/         # Core plugins registering objects
├── api/             # REST API server
├── cli/             # CLI entry point
├── examples/        # Example scenes
├── tests/           # Tests
```
## 📺 Viewer
The Python package is designed to pair with a browser-based 3D viewer built using Three.js and Svelte (not included in this repo). You can send scenes to the viewer via the REST API.

## 📚 Documentation
Coming soon ...

## 🛠️ Roadmap
1. Basic Viewer (and perhaps in jupyter notebooks)
2. Web-based editor UI (Svelte + Three.js)
3. Plugin marketplace system
4. Dynamic data sources & animation support
5. Desktop version via Electron or Tauri (if the web editor was a success)

_Built with 💚 for devs who think in both code and space._
