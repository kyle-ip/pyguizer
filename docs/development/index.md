# Development

This guide will help you set up a development environment for PyGUIzer and contribute to the project.

## Prerequisites

Before you start developing for PyGUIzer, ensure you have the following installed:

- **Python 3.10+**: Required for the backend
- **Node.js 16+**: Required for frontend development
- **npm or yarn**: Required for frontend dependencies
- **Git**: For version control

## Setting Up the Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/kyle-ip/pyguizer.git
cd pyguizer
```

### 2. Install Python Dependencies

```bash
# Install in development mode with all dependencies
pip install -e .[dev]

# Install only the basic dependencies
pip install -e .
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

## Project Structure

PyGUIzer has a modular structure organized into backend and frontend components:

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
├── tests/             # Unit and integration tests
├── docs/              # Documentation
├── README.md          # Project README
└── pyproject.toml     # Package configuration
```

## Development Workflow

### Backend Development

1. **Make changes to the Python code** in the `pyguizer/` directory
2. **Run tests** to ensure your changes don't break existing functionality
3. **Test with examples** to verify the behavior

### Frontend Development

1. **Start the frontend development server**:
   ```bash
   cd frontend
   npm run dev
   ```

2. **Start the backend server** in a separate terminal:
   ```bash
   python -m pyguizer run examples/advanced_features.py
   ```

3. **Make changes to the frontend code** in the `frontend/src/` directory
4. **See changes live** in your browser

### Building the Frontend

When you're ready to build the frontend for production:

```bash
cd frontend
npm run build
```

This will create a production build in the `frontend/build/` directory, which will be served by the backend.

## Running Tests

PyGUIzer includes a comprehensive test suite:

### Running All Tests

```bash
python -m pytest
```

### Running Specific Test Modules

```bash
# Run core tests
python -m pytest tests/test_core.py -v

# Run verification tests
python -m pytest tests/verify_core.py -v
```

### Test Coverage

```bash
python -m pytest --cov=pyguizer tests/
```

## Code Quality

PyGUIzer follows strict code quality standards:

### Formatting

```bash
# Format Python code with black
black pyguizer/

# Sort imports with isort
isort pyguizer/

# Format frontend code with Prettier
cd frontend
npm run format
```

### Linting

```bash
# Lint Python code with flake8
flake8 pyguizer/

# Lint frontend code with ESLint
cd frontend
npm run lint
```

## Contributing

We welcome contributions to PyGUIzer! Please follow these guidelines:

### 1. Fork the Repository

Create a fork of the PyGUIzer repository on GitHub.

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

Implement your feature or fix, following the code quality guidelines.

### 4. Write Tests

Add tests for your changes to ensure they work correctly and don't break existing functionality.

### 5. Submit a Pull Request

Push your changes to your fork and submit a pull request to the main repository.

## Code of Conduct

Please adhere to our [Code of Conduct](../CODE_OF_CONDUCT.md) in all interactions.

## Development Roadmap

Check the [project roadmap](../roadmap.md) for upcoming features and planned improvements.
