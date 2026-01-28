# Features

PyGUIzer offers a comprehensive set of features to simplify the creation of GUI applications from Python functions.

## Available Features

### Core Features

- **Function Introspection**: Automatically analyze function signatures and docstrings
- **Widget Generation**: Create appropriate UI components based on parameter types
- **Layout Management**: Intelligent arrangement of UI elements
- **Function Execution**: Run both synchronous and asynchronous functions
- **Batch Processing**: Execute multiple functions concurrently
- **Preset Management**: Save and load function parameter presets

### Advanced Features

#### [Widget Types](widgets.md)
- Support for basic types (str, int, float, bool)
- Complex types (List, Dict, Tuple, Set)
- Specialized types (UUID, Decimal, Path, Enum)
- DateTime types (date, time, datetime)
- Custom type mappings

#### [Pipelines](pipelines.md)
- Create directed acyclic graphs (DAGs) of functions
- Support for serial and parallel execution modes
- Handle both sync and async function nodes
- Automatic dependency management
- Real-time execution status updates
- Comprehensive API for pipeline management

### Technical Features

- **FastAPI Backend**: Modern, high-performance API framework
- **WebSocket Support**: Real-time communication for execution updates
- **Type Safety**: Pydantic models for request/response validation
- **Async Support**: Native asynchronous function execution
- **Concurrency**: Parallel processing capabilities
- **Extensible Architecture**: Modular design for easy customization

### Deployment Features

- **Docker Support**: Containerization for consistent deployment
- **Packaging**: Optimized PyInstaller configuration
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Lightweight**: Minimal dependencies and efficient resource usage

## Getting Started

To explore these features, start with the [Quick Start](../getting-started/quick-start.md) guide and then dive into the specific feature documentation.
