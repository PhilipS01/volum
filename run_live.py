import argparse, uvicorn, runpy, os
from pathlib import Path
from volum.config.runtime import runtime_config
from volum.core import Scene


def extract_scene_path(python_path: Path) -> Path:
    """Extract the scene path from a Python script by monkey-patching the Scene.save method.

    Args:
        python_path (Path): The path to the Python script to run.

    Raises:
        RuntimeError: If the scene path cannot be determined.

    Returns:
        Path: The resolved path to the scene JSON file.
    """

    saved_path = {} # mutable dict to store the path
    original_save = Scene.save

    def patched_save(self, path: str=os.path.join(os.getcwd(), "scene.json"), *args, **kwargs):
        saved_path["path"] = path
        return original_save(self, path, *args, **kwargs)

    Scene.save = patched_save # monkey-patch the save method

    try:
        runpy.run_path(str(python_path), run_name="__main__") # run the script to trigger the save method
    finally:
        Scene.save = original_save

    if "path" not in saved_path:
        raise RuntimeError("Could not determine scene path. Script must call scene.save(path)")

    return Path(saved_path["path"]).resolve()


def main():
    parser = argparse.ArgumentParser(
        description="Run the Volum live viewer with configurable scene and volume paths"
    )
    parser.add_argument(
        "--python-path",
        help="Path to the python script to watch and run (containing a scene object)"
    )
    parser.add_argument(
        "--scene-path",
        help="Optional: JSON scene file to serve. Required if --python-path is not provided."
    )
    parser.add_argument(
        "--host", default="127.0.0.1",
        help="Host interface to bind the server"
    )
    parser.add_argument(
        "--port", type=int, default=8000,
        help="Port number for the server"
    )
    args = parser.parse_args()

    # Validate that at least one input path is provided
    if not args.scene_path and not args.python_path:
        parser.error("You must provide at least --scene-path or --python-path.")

    # Resolve the scene path
    if args.scene_path:
        scene_path = Path(args.scene_path).resolve()
    else:
        python_path = Path(args.python_path).resolve()
        if not python_path.exists() or not python_path.suffix == ".py":
            parser.error(f"Provided python path is invalid or not a .py file: {python_path}")
        scene_path = extract_scene_path(python_path)

    # Set up runtime configuration
    runtime_config.scene_path = scene_path
    runtime_config.python_path = Path(args.python_path).resolve() if args.python_path else None

    uvicorn_args = {
        "app": "volum.api:app",
        "host": args.host,
        "port": args.port,
    }

    uvicorn.run(**uvicorn_args)
    # Open the viewer in the default web browser
    #time.sleep(1)  # wait a bit for server to start
    #webbrowser.open(f"http://{args.host}:{args.port}/")


if __name__ == "__main__":
    main()
