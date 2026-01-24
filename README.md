# PyGUIzer

![PyGUIzer](https://img.shields.io/badge/PyGUIzer-Automatic%20Web%20GUI%20Generator-blueviolet)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Documentation](https://img.shields.io/badge/Docs-Read%20the%20Docs-blue)

Automatically generate interactive, production-ready web GUI applications from standard Python function signatures and type hints. PyGUIzer bridges the gap between Python's powerful backend logic and accessible user interfaces, enabling rapid prototyping and deployment with zero frontend code.

## ✨ Features

### Core Functionality
- **Automatic UI Generation**: Create complete web GUIs from Python function signatures alone
  - 📝 Clean, modern design with responsive layout
  - 🎨 Consistent styling across all widgets
  - 🌟 Interactive controls with real-time feedback
  - 📱 Responsive design for different screen sizes
  - 🎯 Built on FastAPI and React for robust, scalable applications
- **Advanced Intelligent Type Mapping**: Smart conversion of 15+ Python types to appropriate UI widgets
  - Basic types: `str`, `int`, `float`, `bool`
  - Complex types: `List`, `Set`, `Dict`, `Tuple`, `FrozenSet`
  - Specialized types: `UUID`, `Decimal`, `Path`, `Enum`
  - DateTime types: `date`, `time`, `datetime`
  - Custom types: Dataclasses, third-party library classes
- **Enhanced Custom Widget Registry**: Flexible system for extending widget support
  - Direct type mappings
  - Inheritance-based mappings with priority levels
  - String-based mappings for dynamic types
  - Easy API for registering custom widgets

### User Experience
- **Preset Management**: Save and load input configurations
  - Full CRUD operations for presets
  - Intuitive UI with modal dialogs
  - Support for all parameter types
- **Markdown Rendering**: Rich output display for markdown-formatted results
  - Headers, lists, tables, code blocks, quotes, and links
  - Styled components with consistent design
  - Syntax highlighting for code blocks
- **Real-Time Updates**: WebSocket support for live task status
  - Progress tracking with percentage indicators
  - Streaming output support
  - Task cancellation functionality

### Developer Experience
- **Clean API**: Designed for "vibe coding" with AI assistant support
- **Full Customization**: Escape hatches for complete UI and behavior control
- **Production-Ready**: Built on battle-tested frameworks
- **Open & Extensible**: Community-driven ecosystem for widgets, themes, and integrations
- **Cross-Platform**: Deploy as web services or desktop applications

### Deployment Options
- **Web Server**: FastAPI server with built-in static file serving
- **Desktop App**: Future support for Tauri integration
- **Docker**: Production-optimized Dockerfile generation
- **Framework Integration**: Mount into existing FastAPI/Flask applications

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

### Comprehensive Type-to-Widget Mapping

PyGUIzer automatically maps 15+ Python types to appropriate UI widgets:

| Python Type | Widget Type  | Example                  | Features |
| ----------- | ------------ | ------------------------ | -------- |
| **Basic Types** | | | |
| `str`       | Text Input   | `name: str`              | Simple text input with placeholder |
| `int`       | Number Input | `age: int`               | Integer-only input with min/max support |
| `float`     | Slider       | `temperature: float`     | Interactive slider with visual feedback |
| `bool`      | Checkbox     | `is_active: bool`        | Toggle switch with clear state indication |
| **Complex Types** | | | |
| `List[str]` | Multi-select | `hobbies: List[str]`     | Multi-selection dropdown for string lists |
| `Set[str]`  | Multi-select | `tags: Set[str]`         | Similar to List but enforces uniqueness |
| `Dict`      | JSON Editor  | `config: Dict[str, Any]` | Full-featured JSON editor for complex data |
| `Tuple`     | JSON Editor  | `dimensions: Tuple[int, int]` | Structured JSON editing for fixed-size collections |
| `FrozenSet` | Multi-select | `unique_values: FrozenSet[str]` | Immutable set with multi-select interface |
| `Any`       | Text Input   | `dynamic: Any`           | Flexible input for dynamic types |
| **Specialized Types** | | | |
| `UUID`      | Text Input   | `user_id: UUID`          | Validated input with UUID format checking |
| `Decimal`   | Number Input | `price: Decimal`         | High-precision decimal input |
| `Path`      | File Upload  | `file: Path`             | File selection widget with upload capabilities |
| `Enum`      | Select       | `color: Color`           | Dropdown with auto-generated enum options |
| **DateTime Types** | | | |
| `date`      | Date Picker  | `birth_date: date`       | Calendar widget for date selection |
| `time`      | Time Picker  | `meeting_time: time`     | Time selection widget with format support |
| `datetime`  | DateTime Picker | `event: datetime`     | Combined date and time selection |
| **Custom Types** | | | |
| Dataclass   | JSON Editor  | `user: User`             | Smart handling of dataclass structures |
| Third-party | Auto-mapped  | `third_party: LibraryClass` | Inheritance-based mapping for external classes |

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

### Preset Management

Save and load input configurations with the built-in preset management system:

```python
from pyguizer import PyGUIzer

@PyGUIzer()
def advanced_profile(
    name: str = "World",
    age: int = 30,
    height: float = 1.75,
    is_active: bool = True,
    colors: List[str] = None
) -> Dict[str, any]:
    # Function implementation
    pass
```

**Usage in UI:**
1. Fill in your desired inputs
2. Click "Save Current Inputs as Preset" to save
3. Enter a name and optional description
4. Load presets later from the preset list
5. Delete presets you no longer need

### Markdown Rendering

Generate rich, formatted output with built-in markdown rendering support:

```python
from pyguizer import PyGUIzer

@PyGUIzer()
def generate_markdown_report(
    title: str = "Sample Report",
    include_list: bool = True,
    include_table: bool = True,
    include_code: bool = True
) -> str:
    """Generate a comprehensive markdown report"""
    report = [f"# {title}"]
    
    if include_list:
        report.extend([
            "## Features",
            "- Advanced type support",
            "- Preset management",
            "- Markdown rendering",
            "- Real-time updates"
        ])
    
    if include_table:
        report.extend([
            "## Performance",
            "| Metric | Value |",
            "|--------|-------|",
            "| Speed  | Fast  |",
            "| Scalability | High |",
            "| Reliability | Excellent |"
        ])
    
    if include_code:
        report.extend([
            "## Code Example",
            "```python",
            "def hello(name):",
            "    return f'Hello, {name}!',",
            "```"
        ])
    
    return "\n\n".join(report)
```

**Markdown Features Supported:**
- Headers (H1-H6)
- Unordered and ordered lists
- Tables with styled formatting
- Code blocks with syntax highlighting
- Inline code formatting
- Blockquotes
- External links
- Proper spacing and styling

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

## 🛠️ Enhanced Custom Widget Registry

Extend PyGUIzer with custom widget mappings for your own types or third-party libraries:

```python
from pyguizer.core.widget import register_widget_mapping, WidgetType
from your_library import CustomType

# Register a custom mapping with priority
def custom_widget_generator(py_type):
    return WidgetType.JSON, {"description": "Custom type editor"}

# Register for direct type mapping and inheritance
register_widget_mapping(CustomType, custom_widget_generator, priority=10)

# Usage in your function
from pyguizer import PyGUIzer

@PyGUIzer()
def process_data(custom_input: CustomType) -> str:
    return f"Processed: {custom_input}"
```

**Registry Features:**
- Multiple mapping types: direct, inheritance-based, string-based
- Priority levels for resolving conflicts
- Support for third-party library classes
- Easy-to-use API for registration

## 📁 Project Structure

```
pyguizer/
├── pyguizer/          # Main package
│   ├── __init__.py     # Package entry point
│   ├── cli.py         # CLI implementation
│   ├── api/           # FastAPI application
│   │   └── app.py      # API endpoints and WebSocket support
│   └── core/          # Core functionality
│       ├── introspection.py  # Function signature analysis
│       ├── widget.py          # Widget specification generation & registry
│       └── layout.py          # Layout processing
├── frontend/          # React frontend
│   ├── src/           # Source code
│   │   ├── App.tsx     # Main application component
│   │   ├── components/ # React components
│   │   │   └── WidgetFactory.tsx # Widget rendering
│   │   ├── services/   # API client and WebSocket manager
│   │   └── types/      # Type definitions
│   └── package.json    # Frontend dependencies
├── examples/          # Example applications
│   └── sample_app.py   # Comprehensive example with all features
├── tests/             # Unit and integration tests
├── docs/              # Documentation
│   ├── DEVELOPMENT_PROGRESS.md # Implementation details
│   ├── TECHNICAL_SOLUTION.md   # Architecture documentation
│   └── GIT_CONVENTIONAL_COMMIT.md # Commit guidelines
├── README.md          # This file
└── pyproject.toml     # Package configuration
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

## 🚀 Roadmap

### ✅ Completed (Phase 2 - POC)

1. **Advanced Type Support**: 15+ parameter types including UUID, Decimal, Date, Time, Set, Tuple, FrozenSet, and dataclasses
2. **Enhanced Custom Widget Registry**: Support for direct, inheritance-based, and string-based mappings
3. **Preset Management System**: Full CRUD operations with UI integration
4. **Markdown Rendering Support**: Comprehensive formatting for rich output display
5. **Real-time WebSocket Communication**: Task updates and bidirectional communication
6. **Comprehensive Task Management**: Asynchronous execution with status tracking

### 📅 Phase 3 - Production Ready

#### Core Functionality
1. **Enhanced Layout System**: Tabs, accordions, and complex layouts
2. **Theming Support**: Light/dark themes and custom styling
3. **Advanced Validation**: Real-time input validation with custom error messages
4. **Input History**: Undo/redo functionality for inputs

#### Deployment Options
5. **Tauri Integration**: Desktop app build support
6. **Docker Support**: Production-optimized Dockerfiles
7. **Framework Integration**: Mount into existing FastAPI/Flask applications

#### Security & Performance
8. **Security Enhancements**: Input sanitization and secure execution modes
9. **Performance Optimization**: Widget rendering and API response times
10. **Caching Mechanisms**: App specification and request caching

#### Developer Experience
11. **Improved CLI Tools**: Project scaffolding, building, deployment
12. **Comprehensive Documentation**: Tutorials and use cases
13. **Testing Framework**: Comprehensive testing for both backend and frontend

## 🤝 Contributing

Contributions are welcome! Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Code of Conduct

Please adhere to our [Code of Conduct](docs/CODE_OF_CONDUCT.md) in all interactions.

## 📄 License

PyGUIzer is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/kyle-ip/pyguizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kyle-ip/pyguizer/discussions)
- **Source Code**: [GitHub Repository](https://github.com/kyle-ip/pyguizer)

## 🙏 Acknowledgments

PyGUIzer was inspired by the need to bridge the gap between Python's powerful backend ecosystem and accessible user interfaces. Special thanks to all contributors and the open-source community for their support.

Built with:
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.10+ based on standard Python type hints
- **React**: A JavaScript library for building user interfaces
- **TypeScript**: A typed superset of JavaScript that compiles to plain JavaScript
- **Vite**: Next generation frontend tooling
- **Axios**: Promise based HTTP client for the browser and node.js

PyGUIzer is designed to work seamlessly with AI assistants for "vibe coding", allowing developers to rapidly prototype and deploy applications with minimal effort.