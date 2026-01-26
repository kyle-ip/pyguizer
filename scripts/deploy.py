"""
PyGUIzer Deployment Script

This script demonstrates how to package a PyGUIzer application into a standalone executable.
"""

import os
import shutil
import subprocess
import sys
import tempfile


def deploy_pyguizer_app(file_path, name=None, output_dir="./dist", onefile=True, windowed=True):
    """
    Package a PyGUIzer application into a standalone executable.
    
    Args:
        file_path: Path to the Python file containing the PyGUIzer-decorated function
        name: Name for the executable (default: same as input file)
        output_dir: Output directory for the executable
        onefile: Create a single-file executable
        windowed: Create a windowed (GUI) executable without console
    """
    print(f"📦 Packaging PyGUIzer application...")
    
    # Validate the file path
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return 1

    if not file_path.endswith(".py"):
        print(f"Error: File must be a Python file (.py): {file_path}")
        return 1

    # Get the output name
    if name is None:
        name = os.path.splitext(os.path.basename(file_path))[0]

    print(f"📦 Application name: {name}")

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
    except ImportError:
        print("📥 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Create temporary directory for building
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Created temporary build directory: {temp_dir}")

        # Copy the user's script to the temp directory
        user_script = os.path.join(temp_dir, "app.py")
        shutil.copy2(file_path, user_script)

        # Create a main entry point that runs the PyGUIzer app
        main_script = os.path.join(temp_dir, "main.py")
        with open(main_script, "w", encoding="utf-8") as f:
            f.write("import sys\n")
            f.write("import uvicorn\n")
            f.write("import asyncio\n")
            f.write("from contextlib import suppress\n\n")
            f.write("# Add the current directory to path to import app.py\n")
            f.write("sys.path.insert(0, '.')\n\n")
            f.write("# Import the user's app\n")
            f.write("import app\n\n")
            f.write("# Create a simple HTTP server wrapper\n")
            f.write("async def start_server():\n")
            f.write("    \"\"\"Start the PyGUIzer server and open browser.\"\"\"\n")
            f.write("    import webbrowser\n")
            f.write("    import time\n\n")
            f.write("    # Find the PyGUIzer instance or create one\n")
            f.write("    pyguizer_instance = None\n")
            f.write("    decorated_functions = []\n")
            f.write("    # First, look for existing PyGUIzer instances and decorated functions\n")
            f.write("    for name, obj in app.__dict__.items():\n")
            f.write("        if hasattr(obj, '__class__') and obj.__class__.__name__ == 'PyGUIzer':\n")
            f.write("            pyguizer_instance = obj\n")
            f.write("        elif callable(obj) and hasattr(obj, '__pyguizer__'):\n")
            f.write("            if pyguizer_instance is None:\n")
            f.write("                pyguizer_instance = obj.__pyguizer__\n")
            f.write("            decorated_functions.append(obj)\n\n")
            f.write("    # If no PyGUIzer instance found, create one and auto-register functions\n")
            f.write("    if not pyguizer_instance:\n")
            f.write("        print(\"Info: No PyGUIzer instance found, creating new one...\")\n")
            f.write("        from pyguizer import PyGUIzer\n")
            f.write("        pyguizer_instance = PyGUIzer()\n\n")
            f.write("    # Auto-register all callable functions if no decorated functions found\n")
            f.write("    if not decorated_functions:\n")
            f.write("        print(\"Info: No decorated functions found, auto-registering all callable functions...\")\n")
            f.write("        for name, obj in app.__dict__.items():\n")
            f.write("            if callable(obj) and not name.startswith('_'):  # Skip private functions\n")
            f.write("                try:\n")
            f.write("                    # Check if it's a function from the app module\n")
            f.write("                    if hasattr(obj, '__module__') and obj.__module__ == 'app':\n")
            f.write("                        pyguizer_instance.register_function(obj)\n")
            f.write("                        decorated_functions.append(obj)\n")
            f.write("                except Exception as e:\n")
            f.write("                    print(f\"Warning: Could not register function {name}: {e}\")\n\n")
            f.write("    if not decorated_functions:\n")
            f.write("        # Try one more approach - check all callable objects\n")
            f.write("        for name, obj in app.__dict__.items():\n")
            f.write("            if callable(obj):\n")
            f.write("                try:\n")
            f.write("                    pyguizer_instance.register_function(obj)\n")
            f.write("                    decorated_functions.append(obj)\n")
            f.write("                except Exception as e:\n")
            f.write("                    pass\n\n")
            f.write("    if not decorated_functions:\n")
            f.write("        print(\"Error: No callable functions found in the script\")\n")
            f.write("        return\n\n")
            f.write("    # Use the first decorated function for the app\n")
            f.write("    func = decorated_functions[0]\n")
            f.write("    print(f\"Info: Using function {func.__name__}\")\n")
            f.write("    # Create the FastAPI app\n")
            f.write("    from pyguizer.api.app import create_app\n")
            f.write("    fastapi_app = create_app(func, pyguizer_instance.layout)\n\n")
            f.write("    # Open browser after a short delay\n")
            f.write("    def open_browser():\n")
            f.write("        time.sleep(2)\n")
            f.write("        webbrowser.open('http://localhost:8000')\n\n")
            f.write("    import threading\n")
            f.write("    threading.Thread(target=open_browser, daemon=True).start()\n\n")
            f.write("    # Configure logging for windowed mode (no console)\n")
            f.write("    import logging\n")
            f.write("    from logging.handlers import RotatingFileHandler\n\n")
            f.write("    # Create a file logger since there's no console in windowed mode\n")
            f.write("    log_file = 'pyguizer_app.log'\n")
            f.write("    logging.basicConfig(\n")
            f.write("        level=logging.INFO,\n")
            f.write("        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\n")
            f.write("        handlers=[\n")
            f.write("            RotatingFileHandler(\n")
            f.write("                log_file,\n")
            f.write("                maxBytes=10*1024*1024,  # 10MB\n")
            f.write("                backupCount=5\n")
            f.write("            )\n")
            f.write("        ]\n")
            f.write("    )\n\n")
            f.write("    # Disable uvicorn's default console logging\n")
            f.write("    uvicorn_log_config = {\n")
            f.write("        'version': 1,\n")
            f.write("        'disable_existing_loggers': False,\n")
            f.write("        'formatters': {\n")
            f.write("            'default': {\n")
            f.write("                '()': 'logging.Formatter',\n")
            f.write("                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',\n")
            f.write("            },\n")
            f.write("        },\n")
            f.write("        'handlers': {\n")
            f.write("            'default': {\n")
            f.write("                'formatter': 'default',\n")
            f.write("                'class': 'logging.handlers.RotatingFileHandler',\n")
            f.write("                'filename': log_file,\n")
            f.write("                'maxBytes': 10*1024*1024,\n")
            f.write("                'backupCount': 5,\n")
            f.write("            },\n")
            f.write("        },\n")
            f.write("        'loggers': {\n")
            f.write("            'uvicorn': {\n")
            f.write("                'handlers': ['default'],\n")
            f.write("                'level': 'INFO',\n")
            f.write("            },\n")
            f.write("            'uvicorn.error': {\n")
            f.write("                'handlers': ['default'],\n")
            f.write("                'level': 'INFO',\n")
            f.write("                'propagate': False,\n")
            f.write("            },\n")
            f.write("            'uvicorn.access': {\n")
            f.write("                'handlers': ['default'],\n")
            f.write("                'level': 'INFO',\n")
            f.write("                'propagate': False,\n")
            f.write("            },\n")
            f.write("        },\n")
            f.write("    }\n\n")
            f.write("    # Run the server with custom logging configuration\n")
            f.write("    config = uvicorn.Config(\n")
            f.write("        fastapi_app,\n")
            f.write("        host=\"127.0.0.1\",\n")
            f.write("        port=8000,\n")
            f.write("        log_level=\"info\",\n")
            f.write("        log_config=uvicorn_log_config\n")
            f.write("    )\n")
            f.write("    server = uvicorn.Server(config)\n")
            f.write("    await server.serve()\n\n")
            f.write("# Main entry point\n")
            f.write("if __name__ == \"__main__\":\n")
            f.write("    print(\"PyGUIzer Application\")\n")
            f.write("    print(\"Opening browser to http://localhost:8000...\")\n")
            f.write("    print(\"Press Ctrl+C to exit\")\n\n")
            f.write("    # Run the server with asyncio\n")
            f.write("    with suppress(KeyboardInterrupt):\n")
            f.write("        asyncio.run(start_server())\n\n")
            f.write("    print(\"\\nGoodbye!\")\n")
        
        # Copy frontend/build directory to temp dir so PyInstaller can include it
        print("📁 Copying frontend build files...")
        frontend_src = os.path.join(os.path.dirname(__file__), "..", "frontend", "build")
        frontend_dest = os.path.join(temp_dir, "frontend", "build")
        if os.path.exists(frontend_src):
            shutil.copytree(frontend_src, frontend_dest, dirs_exist_ok=True)
        else:
            print("⚠️  Frontend build directory not found. Building frontend...")
            # Build frontend if it doesn't exist
            frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
            subprocess.check_call(["npm", "install"], cwd=frontend_dir)
            subprocess.check_call(["npm", "run", "build"], cwd=frontend_dir)
            shutil.copytree(frontend_src, frontend_dest, dirs_exist_ok=True)
        
        # Build the executable with PyInstaller
        print("🔨 Building executable with PyInstaller...")
        pyinstaller_args = [
            sys.executable,
            "-m", "PyInstaller",
            "--name", name,
            "--distpath", output_dir,
            "--workpath", os.path.join(temp_dir, "build"),
            "--specpath", temp_dir,
            # Include frontend/build directory
            f"--add-data=frontend/build{os.pathsep}frontend/build",
        ]
        
        if onefile:
            pyinstaller_args.append("--onefile")
        
        if windowed:
            pyinstaller_args.extend(["--windowed", "--noconsole"])
        
        # Add hidden imports if needed
        pyinstaller_args.extend([
            "--hidden-import", "uvicorn",
            "--hidden-import", "fastapi",
            "--hidden-import", "pydantic",
            "--hidden-import", "pydantic_core",
            "--hidden-import", "starlette",
            "--hidden-import", "typer",
            "--hidden-import", "pyguizer",
            "--hidden-import", "pyguizer.core",
            "--hidden-import", "pyguizer.api",
        ])
        
        # Add the main script as the entry point
        pyinstaller_args.append(main_script)
        
        print(f"📋 PyInstaller command: {' '.join(pyinstaller_args)}")
        
        # Run PyInstaller
        try:
            subprocess.check_call(pyinstaller_args)
        except subprocess.CalledProcessError as e:
            print(f"Error: PyInstaller failed with exit code {e.returncode}")
            return 1

    # Success message
    print("\n✅ Packaging completed successfully!")
    print(f"📦 Executable created: {os.path.join(output_dir, name)}{'.exe' if sys.platform == 'win32' else ''}")
    print("\n🚀 To run your standalone application:")
    print(f"   Double-click the executable or run: {os.path.join(output_dir, name)}{'.exe' if sys.platform == 'win32' else ''}")
    print("\n💡 The application will automatically open in your browser.")
    print("   Press Ctrl+C in the console (if visible) to stop the server.")
    
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy.py <file_path> [--name NAME] [--output_dir DIR] [--onefile True/False] [--windowed True/False]")
        sys.exit(1)
    
    # Parse arguments
    file_path = sys.argv[1]
    name = None
    output_dir = "./dist"
    onefile = True
    windowed = True
    
    # Simple argument parsing for demonstration
    for arg in sys.argv[2:]:
        if arg.startswith("--name="):
            name = arg.split("=", 1)[1]
        elif arg.startswith("--output_dir="):
            output_dir = arg.split("=", 1)[1]
        elif arg.startswith("--onefile="):
            onefile = arg.split("=", 1)[1].lower() == "true"
        elif arg.startswith("--windowed="):
            windowed = arg.split("=", 1)[1].lower() == "true"
    
    sys.exit(deploy_pyguizer_app(file_path, name, output_dir, onefile, windowed))
