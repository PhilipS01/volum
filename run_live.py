import argparse, os, uvicorn
from pathlib import Path
from volum.config.runtime import runtime_config



def main():
    parser = argparse.ArgumentParser(
        description="Run the Volum live viewer with configurable scene and volume paths"
    )
    parser.add_argument(
        "--scene-path", required=True,
        help="Path to the scene JSON file to watch and serve, or output path of python script if python-path is provided too."
    )
    parser.add_argument(
        "--python-path", required=False,
        help="Path to the python script to watch and run (containing a scene object)"
    )
    parser.add_argument(
        "--host", default="127.0.0.1",
        help="Host interface to bind the server"
    )
    parser.add_argument(
        "--port", type=int, default=8000,
        help="Port number for the server"
    )
    parser.add_argument(
        "--reload", action="store_true",
        help="Enable auto-reload on code changes (uvicorn --reload)"
    )
    args = parser.parse_args()

    # Set up runtime configuration
    runtime_config.scene_path = Path(args.scene_path).resolve()
    runtime_config.python_path = Path(args.python_path).resolve() if args.python_path else None

    uvicorn_args = {
        "app": "volum.api:app",
        "host": args.host,
        "port": args.port,
    }
    if args.reload:
        uvicorn_args["reload"] = True

    uvicorn.run(**uvicorn_args)
    # Open the viewer in the default web browser
    #time.sleep(1)  # wait a bit for server to start
    #webbrowser.open(f"http://{args.host}:{args.port}/")


if __name__ == "__main__":
    main()
