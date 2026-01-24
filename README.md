# PyGUIzer

![PyGUIzer](https://img.shields.io/badge/PyGUIzer-Automatic%20Web%20GUI%20Generator-blueviolet)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Documentation](https://img.shields.io/badge/Docs-Read%20the%20Docs-blue)

Automatically generate interactive, production-ready web GUI applications from standard Python function signatures and type hints. PyGUIzer bridges the gap between Python's powerful backend logic and accessible user interfaces, enabling rapid prototyping and deployment with zero frontend code.

## ✨ Features

- **Automatic UI Generation**: Create complete web (hand-drawn style) GUIs from Python function signatures alone
  - 📝 Comic-style font for a playful feel
  - 🎨 Sketchy borders and paper-like background
  - 🔄 Subtle rotations for each section
  - 🌟 Animated buttons with hover effects
  - 🎛️ Fun, interactive sliders and checkboxes
  - 📱 Responsive design for different screen sizes
- **Intelligent Type Mapping**: Smart conversion of Python types to appropriate UI widgets
- **Developer Experience First**: Clean API designed for "vibe coding" with AI assistant support
- **Production-Ready**: Built on FastAPI and React for robust, scalable applications
- **Full Customization**: Escape hatches for complete UI and behavior control
- **Open & Extensible**: Community-driven ecosystem for widgets, themes, and integrations
- **Cross-Platform**: Deploy as web services or desktop applications

## 🚀 Quick Start

### Installation

```bash
# Install with pip
pip install pyguizer

# Install from source
git clone https://github.com/kyle-ip/pyguizer.git
cd pyguizer
pip install -e .
```

### Basic Usage

```python
from typing import List
from pyguizer import PyGUIzer

@PyGUIzer()
def greet(name: str, age: int, hobbies: List[str] = None) -> str:
    """Generate a personalized greeting message."""
    hobbies_str = f" and enjoy {', '.join(hobbies)}" if hobbies else ""
    return f"Hello {name}! You are {age} years old{hobbies_str}."

# Run directly if this file is executed
if __name__ == "__main__":
    from pyguizer.api.app import create_app
    import uvicorn
    app = create_app(greet)
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Run with CLI

```bash
# Create a sample file
cat > app.py << 'EOF'
from typing import List
from pyguizer import PyGUIzer

@PyGUIzer()
def greet(name: str, age: int, hobbies: List[str] = None) -> str:
    """Generate a greeting message."""
    hobbies_str = f" and enjoy {', '.join(hobbies)}" if hobbies else ""
    return f"Hello {name}! You are {age} years old{hobbies_str}."
EOF

# Run with PyGUIzer CLI
python -m pyguizer run app.py
```

Open your browser to `http://localhost:8000` to see your generated GUI!

## 📖 Detailed Usage

### Type-to-Widget Mapping

PyGUIzer automatically maps Python types to appropriate UI widgets:

| Python Type | Widget Type  | Example                  |
| ----------- | ------------ | ------------------------ |
| `str`       | Text Input   | `name: str`              |
| `int`       | Number Input | `age: int`               |
| `float`     | Slider       | `temperature: float`     |
| `bool`      | Checkbox     | `is_active: bool`        |
| `List[str]` | Multi-select | `hobbies: List[str]`     |
| `Dict`      | JSON Editor  | `config: Dict[str, Any]` |

### Layout Customization

Customize the UI layout using a simple configuration:

```python
from pyguizer import PyGUIzer

layout = {
    "sections": [
        {
            "name": "Personal Info",
            "widgets": ["name", "age"]
        },
        {
            "name": "Preferences",
            "widgets": ["hobbies", "is_active"]
        }
    ]
}

@PyGUIzer(layout=layout)
def greet(name: str, age: int, hobbies: List[str] = None, is_active: bool = True) -> str:
    # Function implementation
    pass
```

### Multiple Functions

PyGUIzer supports multiple decorated functions in a single file:

```python
from pyguizer import PyGUIzer

@PyGUIzer()
def greet(name: str, age: int) -> str:
    return f"Hello {name}!"

@PyGUIzer()
def calculate(a: float, b: float, operation: str = "add") -> float:
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y
    }
    return operations[operation](a, b)
```

## 📁 Project Structure

```
pyguizer/
├── pyguizer/          # Main package
│   ├── __init__.py     # Package entry point
│   ├── cli.py         # CLI implementation
│   ├── api/           # FastAPI application
│   └── core/          # Core functionality
│       ├── introspection.py  # Function signature analysis
│       ├── widget.py          # Widget specification generation
│       └── layout.py          # Layout processing
├── frontend/          # React frontend
├── examples/          # Example applications
├── tests/             # Unit and integration tests
├── docs/              # Documentation
├── README.md
└── pyproject.toml
```

## 🛠️ Development

### Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn

### Setup

```bash
# Clone the repository
git clone https://github.com/kyle-ip/pyguizer.git
cd pyguizer

# Install Python dependencies
pip install -e .[dev]

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test modules
python -m pytest tests/test_core.py -v
python -m pytest tests/verify_core.py -v
```

### Code Quality

```bash
# Format code with black
black pyguizer/

# Sort imports with isort
isort pyguizer/

# Check with flake8
flake8 pyguizer/
```

### Building the Frontend

```bash
cd frontend
npm run build
```

## 🤝 Contributing

Contributions are welcome! Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Code of Conduct

Please adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.

## 📄 License

PyGUIzer is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/kyle-ip/pyguizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kyle-ip/pyguizer/discussions)

## 🚀 Roadmap

See our [Technical Solution Document](docs/TECHNICAL_SOLUTION.md) for the complete implementation roadmap.

## 🙏 Acknowledgments

PyGUIzer was inspired by the need to bridge the gap between Python's powerful backend ecosystem and accessible user interfaces. Special thanks to all contributors and the open-source community for their support.