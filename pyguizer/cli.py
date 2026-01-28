"""PyGUIzer CLI Tool"""

# flake8: noqa: E501
import importlib.util
import os
import sys

import typer
import uvicorn

app = typer.Typer(name="pyguizer", help="PyGUIzer CLI Tool")


@app.command(name="run")
def run(
    file_path: str,
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = False,
):
    """Run a PyGUIzer application from a Python file."""
    # Validate the file path
    if not os.path.exists(file_path):
        typer.echo(f"Error: File not found: {file_path}", err=True)
        raise typer.Exit(code=1)

    if not file_path.endswith(".py"):
        typer.echo(f"Error: File must be a Python file (.py): {file_path}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Loading PyGUIzer application from {file_path}...")

    # Add the file's directory to the path
    file_dir = os.path.dirname(os.path.abspath(file_path))
    sys.path.insert(0, file_dir)

    try:
        # Load the module
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            typer.echo(f"Error: Could not load module from {file_path}", err=True)
            raise typer.Exit(code=1)

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Find PyGUIzer decorated functions
        pyguizer_instances = []
        decorated_functions = []

        for name, obj in module.__dict__.items():
            # Check if it's a PyGUIzer instance
            if hasattr(obj, "__class__") and obj.__class__.__name__ == "PyGUIzer":
                pyguizer_instances.append(obj)
            # Check if it's a decorated function
            elif callable(obj) and hasattr(obj, "__pyguizer__"):
                pyguizer_instances.append(obj.__pyguizer__)
                decorated_functions.append(name)

        # If no PyGUIzer instances found, check wrapped functions
        if not pyguizer_instances:
            for name, obj in module.__dict__.items():
                if callable(obj) and hasattr(obj, "__wrapped__"):
                    if hasattr(obj.__wrapped__, "__pyguizer__"):
                        pyguizer_instances.append(obj.__wrapped__.__pyguizer__)
                        decorated_functions.append(name)

        if not pyguizer_instances:
            # Try checking all objects in the module
            for name, obj in module.__dict__.items():
                if hasattr(obj, "__pyguizer__"):
                    pyguizer_instances.append(obj.__pyguizer__)
                    decorated_functions.append(name)

        if not pyguizer_instances:
            # No PyGUIzer-decorated functions found, auto-register all callable functions
            from pyguizer import PyGUIzer

            typer.echo(
                f"Info: No PyGUIzer-decorated functions found, auto-registering all callable functions in {file_path}"
            )

            # Create a new PyGUIzer instance
            auto_pyguizer = PyGUIzer()

            # Register all callable functions from the module
            for name, obj in module.__dict__.items():
                if callable(obj) and not name.startswith("_"):  # Skip private functions
                    try:
                        # Check if it's a built-in function or imported function
                        if (
                            hasattr(obj, "__module__")
                            and obj.__module__ == module.__name__
                        ):
                            auto_pyguizer.register_function(obj)
                            decorated_functions.append(name)
                    except Exception as e:
                        typer.echo(
                            f"Warning: Could not register function {name}: {e}",
                            err=True,
                        )

            if decorated_functions:
                pyguizer_instances = [auto_pyguizer]
                typer.echo(
                    f"Info: Auto-registered {len(decorated_functions)} functions: {', '.join(decorated_functions)}"
                )
            else:
                # Try one more approach - check all functions in the module
                for name, obj in module.__dict__.items():
                    if callable(obj):
                        try:
                            auto_pyguizer.register_function(obj)
                            decorated_functions.append(name)
                        except Exception:
                            continue

                if decorated_functions:
                    pyguizer_instances = [auto_pyguizer]
                    typer.echo(
                        f"Info: Auto-registered {len(decorated_functions)} functions: {', '.join(decorated_functions)}"
                    )
                else:
                    typer.echo(
                        f"Error: No callable functions found in {file_path}", err=True
                    )
                    raise typer.Exit(code=1)

        # For now, use the first PyGUIzer instance
        pyguizer_instance = pyguizer_instances[0]

        if len(decorated_functions) > 1:
            typer.echo(
                f"Info: Found {len(decorated_functions)} PyGUIzer-decorated functions"
            )
            typer.echo(f"Using function: {decorated_functions[0]}")
        else:
            typer.echo(
                f"Info: Found PyGUIzer-decorated function: {decorated_functions[0]}"
            )

    except Exception as e:
        typer.echo(f"Error loading module: {e}", err=True)
        raise typer.Exit(code=1)

    try:
        # Import here to avoid circular imports
        from pyguizer.api.app import create_app

        # Create the FastAPI app
        typer.echo("Creating FastAPI application...")
        fastapi_app = create_app(pyguizer_instance.func, pyguizer_instance.layout)

        # Run the server
        typer.echo(f"\n🚀 Starting PyGUIzer server on http://{host}:{port}...")
        typer.echo(
            f"📖 Open your browser to http://{host}:{port} to see your application"
        )
        typer.echo(f"\n⏹️  Press Ctrl+C to stop the server")
        typer.echo("\n" + "=" * 50)

        uvicorn.run(fastapi_app, host=host, port=port, reload=reload)
    except ImportError as e:
        typer.echo(f"Error importing dependencies: {e}", err=True)
        typer.echo(
            "Hint: Make sure you have installed all required dependencies: fastapi, pydantic, uvicorn"
        )
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error starting server: {e}", err=True)
        raise typer.Exit(code=1)


@app.command(name="init")
def init(
    project_name: str,
):
    """Initialize a new PyGUIzer project."""
    # Create project directory
    project_dir = os.path.join(os.getcwd(), project_name)

    if os.path.exists(project_dir):
        typer.echo(f"Error: Directory {project_dir} already exists", err=True)
        raise typer.Exit(code=1)

    os.makedirs(project_dir, exist_ok=True)

    # Create README.md content using string concatenation to avoid escape issues
    readme_content = f"# {project_name}\n\n"
    readme_content += (
        "A PyGUIzer application automatically generated from Python functions.\n\n"
    )

    readme_content += "## Getting Started\n\n"
    readme_content += "### Installation\n\n"
    readme_content += "```bash\n"
    readme_content += "# Install PyGUIzer\n"
    readme_content += "pip install pyguizer\n\n"
    readme_content += "# Install dependencies\n"
    readme_content += "pip install fastapi pydantic uvicorn\n"
    readme_content += "```\n\n"

    readme_content += "### Running the Application\n\n"
    readme_content += "```bash\n"
    readme_content += "# Run the app with PyGUIzer CLI\n"
    readme_content += "pyguizer run app.py\n\n"
    readme_content += "# Or run directly with Python\n"
    readme_content += "python app.py\n"
    readme_content += "```\n\n"

    readme_content += (
        "Open your browser to `http://localhost:8000` to see the application.\n\n"
    )

    readme_content += "## Project Structure\n\n"
    readme_content += "```\n"
    readme_content += f"{project_name}/\n"
    readme_content += (
        "├── app.py          # Main application file with decorated functions\n"
    )
    readme_content += "└── README.md       # This file\n"
    readme_content += "```\n\n"

    readme_content += "## Adding New Functions\n\n"
    readme_content += "To add a new function to your PyGUIzer application:\n\n"
    readme_content += "1. Add a new function to `app.py`\n"
    readme_content += "2. Decorate it with `@PyGUIzer()`\n"
    readme_content += "3. Run the application again\n\n"

    readme_content += "Example:\n\n"
    readme_content += "```python\n"
    readme_content += "@PyGUIzer()\n"
    readme_content += (
        'def calculate(a: float, b: float, operation: str = "add") -> float:\n'
    )
    readme_content += "    '''Calculate the result of an operation on two numbers.'''\n"
    readme_content += '    if operation == "add":\n'
    readme_content += "        return a + b\n"
    readme_content += '    elif operation == "subtract":\n'
    readme_content += "        return a - b\n"
    readme_content += '    elif operation == "multiply":\n'
    readme_content += "        return a * b\n"
    readme_content += '    elif operation == "divide":\n'
    readme_content += "        return a / b\n"
    readme_content += "    else:\n"
    readme_content += "        return 0\n"
    readme_content += "```\n"

    # Create sample_app content using string concatenation
    sample_app = f"from typing import List, Optional\n"
    sample_app += f"from pyguizer import PyGUIzer\n\n"

    sample_app += f"@PyGUIzer()\n"
    sample_app += f"def greet(name: str, age: int, hobbies: List[str] = None, is_active: bool = True) -> str:\n"
    sample_app += f"    '''Generate a personalized greeting message.'''\n"
    sample_app += (
        f'    hobbies_str = f" and enjoy {{\', \'.join(hobbies)}}" if hobbies else ""\n'
    )
    sample_app += f'    status_str = "active" if is_active else "inactive"\n'
    sample_app += f'    return f"Hello {{{{name}}}}! You are {{{{age}}}} years old, {{{{status_str}}}}{{{{hobbies_str}}}}."\n\n'

    sample_app += f"@PyGUIzer()\n"
    sample_app += f"def calculate_discount(price: float, discount_percentage: float, is_vip: bool = False) -> float:\n"
    sample_app += f"    '''Calculate the final price after applying discounts.'''\n"
    sample_app += f"    base_discount = price * (discount_percentage / 100)\n"
    sample_app += f"    vip_bonus = price * 0.05 if is_vip else 0\n"
    sample_app += f"    total_discount = base_discount + vip_bonus\n"
    sample_app += f"    final_price = price - total_discount\n"
    sample_app += f"    return round(final_price, 2)\n\n"

    sample_app += f"@PyGUIzer()\n"
    sample_app += f'def convert_temperature(celsius: float, to_unit: str = "fahrenheit") -> float:\n'
    sample_app += f"    '''Convert temperature between Celsius and Fahrenheit.'''\n"
    sample_app += f'    if to_unit.lower() == "fahrenheit":\n'
    sample_app += f"        return (celsius * 9/5) + 32\n"
    sample_app += f'    elif to_unit.lower() == "celsius":\n'
    sample_app += f"        return celsius\n"
    sample_app += f"    else:\n"
    sample_app += f"        raise ValueError(\"Invalid unit. Use 'fahrenheit' or 'celsius'.\")\n\n"

    sample_app += f"# Optional: Run the app directly if this file is executed\n"
    sample_app += f'if __name__ == "__main__":\n'
    sample_app += f"    import uvicorn\n"
    sample_app += f"    from pyguizer.api.app import create_app\n    \n"
    sample_app += f"    # Use the first PyGUIzer-decorated function\n"
    sample_app += f"    app = create_app(greet)\n"
    sample_app += f'    uvicorn.run(app, host="0.0.0.0", port=8000)\n'

    # Write files
    with open(os.path.join(project_dir, "README.md"), "w") as f:
        f.write(readme_content)

    with open(os.path.join(project_dir, "app.py"), "w") as f:
        f.write(sample_app)

    typer.echo(f"\n✅ Created new PyGUIzer project in {project_dir}")
    typer.echo(f"\n📁 Project files created:")
    typer.echo(
        f"   - {project_dir}/app.py          # Main application with example functions"
    )
    typer.echo(f"   - {project_dir}/README.md       # Project documentation")

    typer.echo(f"\n🚀 To run your application:")
    typer.echo(f"   cd {project_dir}")
    typer.echo(f"   pyguizer run app.py")

    typer.echo(f"\n📖 Open your browser to http://localhost:8000")

    typer.echo(f"\n💡 Tips:")
    typer.echo(f"   - Add more functions to app.py and decorate them with @PyGUIzer()")
    typer.echo(f"   - Use type hints for automatic widget generation")
    typer.echo(
        f"   - Customize layouts with the layout parameter in @PyGUIzer(layout={...})"
    )


@app.command(name="package")
def package(file_path: str):
    """Package a PyGUIzer application into a standalone executable."""
    import os
    import subprocess
    import sys

    typer.echo(f"📦 Packaging PyGUIzer application from {file_path}...")

    # Get the path to the deployment script
    deploy_script = os.path.join(os.path.dirname(__file__), "../scripts/deploy.py")
    deploy_script = os.path.abspath(deploy_script)

    # Run the deployment script as a subprocess
    result = subprocess.run([sys.executable, deploy_script, file_path], check=False)

    if result.returncode == 0:
        typer.echo("✅ Packaging completed successfully!")
    else:
        typer.echo(f"❌ Packaging failed with exit code {result.returncode}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
