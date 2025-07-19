[![Header](https://github.com/PhilipS01/volum/blob/90af00489989d70374ed29e45c32f310740daca2/docs/static/volum_banner.png)](https://volumeditor.tech/)

[**Volum**](https://volumeditor.tech/) is a modular, extensible Python toolkit for building and rendering interactive 3D scenes that can integrate data visualizations, plots, and geometry — all programmable from Python.

Python has long been the go-to language for data scientists and hobbyists to visualize data in static, two-dimensional formats. Volum transforms this experience by enabling true 3D visualization—making it easy to convert and explore your 2D data in immersive, three-dimensional environments. Because it's **plugins** from the ground up, it makes extending functionality a breeze.

## ✨ Features
- Define 3D scenes programmatically in Python
- **Scriptable** objects (e.g., dynamic data plots, script runner)
- Built-in objects like Box, Sphere, Plane, PlotImage (plt), and Quiver
- Transform objects (position, rotation, scale) with a clean API
- Plugin architecture to add new object types or behaviors
- Scene serialization to JSON (use in viewer or [online editor](https://volumeditor.tech/))
- RESTful interface to sync scene state
- JavaScript scene loader takes scenes and builds them in the browser
- Renders via [Three.js](https://github.com/mrdoob/three.js), with support for more WebGL frameworks coming

## 📦 Installation

Coming soon ...

## 🚀 Quick Example

```python
from volum import Scene
from volum.plugins import BaseShapesPlugin, LightsPlugin, BaseMaterialsPlugin, PlottingPlugin
from volum.objects import *
from volum.core.materials import StandardMaterial, ImageMaterial

scene = Scene()
scene.load_plugins([BaseShapesPlugin(), LightsPlugin(), BaseMaterialsPlugin(), PlottingPlugin()])

# Support for all THREE materials,
box = Transform(object=Box(width=1, height=1, depth=1, material=StandardMaterial(metalness=1, roughness=0)), position=[2, 0, -2], rotation=[45, 0, 0], scale=[1, 1, 1])

# and even image textures.
image_box = Transform(
    object=Box(width=10, height=3.2, depth=.1, material=ImageMaterial()),
    position=[0, 5, -10],
    rotation=[0, 0, 0]
)
scene.add_object(image_box)

# From plotting a simple line in 3D,
line = Line([[0, 0, 0], [0, 2.5, 0], [2, 2.5, -2], [2, 0, -2]])
scene.add_object(line)

# to 3D quivers with 500.000 object instances (unknown data here for demo).
quiver = Quiver(X, Y, Z, U, V, W, colormap="magnitude", colorscheme="inferno")

# Sprinkle some lighting (or alternatively use an environment map, especially with metal materials).
light = Transform(
    object=PointLight(intensity=1),
    position=[0, 50, 20],
    rotation=[0, 0, 0]
)
scene.add_object(light)

# Support for adding objects to the registry via string literals,
scene.add_object("StandardMaterial", name="white_material", color="#fff")
scene.add_object("Box", width=2, height=1, depth=1, material="white_material")

# and changing properties and nest objects after the fact.
box.color = 'cyan'
box = box.transform(rotation=[-45, 0, 0])
scene.add_object(box)

output_path = os.path.join(os.path.dirname(__file__), "test_scene.json")
scene.save(output_path)
```

## 🔌 Plugin System
The plugin system allows developers to extend Volum by adding new object types, behaviors, or utilities without modifying the core library. Each plugin is a Python class that inherits from the ScenePlugin interface and registers new functionality with the internal object registry.

### How It Works:
1. Define a new SceneObject (e.g., a custom geometry or data visualization)
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
scene.save()
```

### Plugin Capabilities:
- New object types (with render and serialization logic)
- Scriptable elements for dynamic behavior
- Scene modifiers (e.g. animations, transformations)
- Custom REST/API integrations or visual widgets (planned)

Plugins can be organized in separate files or even distributed as standalone Python packages for reuse and sharing.

## 🧠 Object Model
Each SceneObject must implement a `to_dict()` method for serialization. Optional interfaces include:
- `Serializable` – provides `to_dict()`
- `Scriptable` – supports dynamic Python scripting (e.g., `run_script(code)`)

Even Materials can be registered as SceneObjects (see example above), when adding them directly via string literals.

## 📁 Project Structure
```
volum/
├── core/            # Scene engine, registry, plugin system
├── objects/         # Built-in object definitions
├── plugins/         # Core plugins registering objects
├── api/             # REST API server
├── config/          # Constants and runtime config
├── docs/            # Documentation and examples
├── tests/           # Tests
viewer/
├── public/          # Static files for viewer
├── src/             # Scene loading, WebSockets, Three.js
```
## 📺 Viewer
The Python package is designed to pair with a browser-based live viewer. The viewer comes with this repository. All you have to do is launching it via run_live.py and providing either the python script path or the serialized scene.json path.
1. **python-path** will automatically run the script, extract where the scene.json is saved, and serve the built scene in the browser
2. **scene-path** will be used to directly provide the viewer with the serialized json, from which the viewer will build the scene

If you make any changes, a **watchdog** will know and re-run the whole thing. No relaoding required.

## 📚 Documentation
Coming soon ...

## 🛠️ Roadmap
1. Basic Viewer (and perhaps in jupyter notebooks)
2. Dynamic data sources & animation support
3. Web-based editor UI (Svelte + Three.js)
4. Plugin marketplace system
5. Desktop version via Electron or Tauri (if the web editor was a success)

_Built with 💜 for devs who think in both code and space._
