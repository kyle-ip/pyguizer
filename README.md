# PyGUIzer

![PyGUIzer](https://img.shields.io/badge/PyGUIzer-Automatic%20Web%20GUI%20Generator-blueviolet)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Documentation](https://img.shields.io/badge/Docs-Read%20the%20Docs-blue)

Automatically generate interactive, production-ready web GUI applications from standard Python function signatures and type hints. PyGUIzer bridges the gap between Python's powerful backend logic and accessible user interfaces, enabling rapid prototyping and deployment with zero frontend code.

![alt text](/docs/image.jpg)

## ✨ Features

### Core Functionality
- **Automatic UI Generation**: Create complete web GUIs from Python function signatures alone
- **Advanced Intelligent Type Mapping**: Smart conversion of 15+ Python types to appropriate UI widgets
- **Enhanced Custom Widget Registry**: Flexible system for extending widget support
- **Smart Auto-Registration**: Works with any Python file without requiring explicit `@PyGUIzer()` decorators
- **Async Function Support**: Native support for both sync and async Python functions
- **Concurrent Processing**: Batch requests are processed concurrently for improved performance

### User Experience
- **Preset Management**: Save and load input configurations
- **Markdown Rendering**: Rich output display for markdown-formatted results
- **Real-Time Updates**: WebSocket support for live task status
- **Dark Mode**: Support for light and dark themes
- **Mobile-Responsive Design**: Adapts to different screen sizes
- **Drag-and-Drop Layout Editor**: Customize UI layouts visually
- **Data Visualization**: Chart.js integration for data charts

### Deployment Options
- **Web Server**: FastAPI server with built-in static file serving
- **Desktop App**: Standalone executable packaging
- **Docker**: Production-optimized Docker containerization
- **Cloud Deployment**: Support for Heroku, AWS, and other cloud platforms

## 📚 Documentation

### Getting Started
- [Installation](docs/getting-started/installation.md): How to install PyGUIzer
- [Quick Start](docs/getting-started/quick-start.md): Basic usage and first steps

### Usage Guide
- [Detailed Usage](docs/usage/index.md): Advanced usage scenarios and examples
- [Layout Customization](docs/usage/index.md#layout-customization): How to customize UI layouts
- [Preset Management](docs/usage/index.md#preset-management): Saving and loading input configurations
- [Markdown Rendering](docs/usage/index.md#markdown-rendering): Creating rich output displays

### Features
- [Widget Types](docs/features/widgets.md): Complete list of supported widgets and type mappings
- [File Uploads](docs/features/widgets.md#file-upload-widget): Handling file uploads with progress tracking
- [Color Picker](docs/features/widgets.md#color-picker-widget): Using color picker widgets
- [Date/Time Pickers](docs/features/widgets.md#date-time-pickers): Working with date and time selection

### Deployment
- [Packaging](docs/deployment/index.md#packaging-as-standalone-executable): Creating standalone executables
- [Docker](docs/deployment/index.md#docker-deployment): Containerized deployment with Docker
- [Web Server](docs/deployment/index.md#web-server-deployment): Deploying as a web service
- [Cloud Deployment](docs/deployment/index.md#cloud-deployment): Deploying to cloud platforms

### API Reference
- [Backend API](docs/api/index.md#backend-api): FastAPI endpoints and WebSocket support
- [Frontend API](docs/api/index.md#frontend-api): React components and services
- [Customization API](docs/api/index.md#customization-api): Widget registry and layout configuration
- [CLI API](docs/api/index.md#cli-api): Command-line interface commands

### Development
- [Development Setup](docs/development/index.md): Setting up a development environment
- [Project Structure](docs/development/index.md#project-structure): Understanding the codebase
- [Contributing](docs/development/index.md#contributing): How to contribute to PyGUIzer

## 🚀 Quick Start

### Installation

```bash
# Install with pip
pip install pyguizer
```

### Basic Usage

Create a Python file with your functions:

```python
# simple_add.py
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def greet(name: str, age: int) -> str:
    """Generate a greeting message."""
    return f"Hello, {name}! You are {age} years old."
```

Run it with PyGUIzer:

```bash
python -m pyguizer run simple_add.py
```

Open your browser to `http://localhost:8000` to see your generated GUI!

## 📁 Project Structure

```
pyguizer/
├── pyguizer/          # Main package
│   ├── __init__.py     # Package entry point
│   ├── cli.py         # CLI implementation
│   ├── api/           # FastAPI application
│   └── core/          # Core functionality
├── frontend/          # React frontend
│   ├── src/           # Source code
│   └── package.json    # Frontend dependencies
├── examples/          # Example applications
│   ├── async_test.py   # Async and concurrent processing example
│   ├── advanced_features.py # Comprehensive feature demonstration
│   └── simple_function.py # Basic usage example
├── tests/             # Unit and integration tests
├── docs/              # Documentation
├── README.md          # This file
└── pyproject.toml     # Package configuration
```

## 🤝 Contributing

Contributions are welcome! Please refer to our [Development Guide](docs/development/index.md#contributing) for guidelines.

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
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs
- **React**: A JavaScript library for building user interfaces
- **TypeScript**: A typed superset of JavaScript
- **Vite**: Next generation frontend tooling
- **Chart.js**: Simple yet flexible JavaScript charting library
- **React DnD**: Drag and drop for React
