# Quick Start

Get up and running with PyGUIzer in minutes! This guide will walk you through creating your first PyGUIzer application.

## Basic Usage

PyGUIzer supports two main approaches to create applications:

### Method 1: Auto-Registration (No Decorators Needed!)

The simplest way to use PyGUIzer is with auto-registration. Just create a Python file with regular functions:

```python
# simple_add.py
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def greet(name: str, age: int) -> str:
    """Generate a greeting message."""
    return f"Hello, {name}! You are {age} years old."
```

Then run it with the PyGUIzer CLI:

```bash
python -m pyguizer run simple_add.py
```

Open your browser to `http://localhost:8000` to see your generated GUI!

### Method 2: Decorator-Based Approach

For more control, use the `@PyGUIzer()` decorator:

```python
# app.py
from pyguizer import PyGUIzer

# Create a PyGUIzer instance
app = PyGUIzer()

@app
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@app
def greet(name: str, age: int) -> str:
    """Generate a greeting message."""
    return f"Hello, {name}! You are {age} years old."

if __name__ == "__main__":
    app.run(title="My First PyGUIzer App", port=8000)
```

Run it directly:

```bash
python app.py
```

## CLI Commands

PyGUIzer provides a simple CLI for running and packaging applications:

### Running Applications

```bash
# Run with auto-registration
python -m pyguizer run path/to/your/file.py

# Run with custom host and port
python -m pyguizer run path/to/your/file.py --host 0.0.0.0 --port 8080
```

### Packaging Applications

```bash
# Package into a standalone executable
python -m pyguizer package path/to/your/file.py

# Package with custom options
python -m pyguizer package path/to/your/file.py --name my_app --output_dir ./build
```

## Next Steps

- Explore the [detailed usage guide](../usage/index.md) for more advanced features
- Learn about [widget types](../features/widgets.md) and how they map from Python types
- Check out [deployment options](../deployment/index.md) for distributing your application
