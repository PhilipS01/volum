import argparse, os, uvicorn, webbrowser, time


def main():
    parser = argparse.ArgumentParser(
        description="Run the Volum live viewer with configurable scene and volume paths"
    )
    parser.add_argument(
        "--scene-path", required=True,
        help="Path to the scene JSON file to watch and serve"
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

    # Export paths as environment variables for the live module to pick up
    os.environ['SCENE_PATH'] = os.path.abspath(args.scene_path)

    uvicorn_args = {
        "app": "volum.api.live:app",
        "host": args.host,
        "port": args.port,
    }
    if args.reload:
        uvicorn_args["reload"] = True

    uvicorn.run(**uvicorn_args)
    # Open the viewer in the default web browser
    time.sleep(1)  # wait a bit for server to start
    webbrowser.open(f"http://{args.host}:{args.port}/")


if __name__ == "__main__":
    main()
