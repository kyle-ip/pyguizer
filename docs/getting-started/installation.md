# Installation

PyGUIzer can be installed through various methods depending on your needs. Choose the approach that best fits your workflow.

## Using pip

The easiest way to install PyGUIzer is through pip:

```bash
# Install with pip
pip install pyguizer
```

## From Source

If you want to install the latest development version or make modifications to PyGUIzer:

```bash
# Clone the repository
git clone https://github.com/kyle-ip/pyguizer.git
cd pyguizer

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e .[dev]
```

## Prerequisites

PyGUIzer requires the following:

- **Python 3.10+**: PyGUIzer uses modern Python features and type hints
- **Node.js 16+** (optional): Only needed if you plan to modify the frontend
- **npm or yarn** (optional): Only needed if you plan to modify the frontend

## Verifying Installation

After installation, you can verify that PyGUIzer is working correctly by running a simple test:

```bash
# Check PyGUIzer version
python -m pyguizer --version

# Run a simple test
python -m pyguizer run examples/simple_function.py
```

Open your browser to `http://localhost:8000` to see the generated GUI!
