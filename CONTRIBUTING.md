# Contributing to PyGUIzer

Thank you for considering contributing to PyGUIzer! We welcome contributions from the community, whether it's bug fixes, feature enhancements, documentation improvements, or new ideas.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Tests](#running-tests)
  - [Code Quality](#code-quality)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
  - [Branching Strategy](#branching-strategy)
  - [Commit Messages](#commit-messages)
  - [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
  - [Python](#python)
  - [Type Hints](#type-hints)
  - [Documentation](#documentation)
- [Testing](#testing)
- [License](#license)

## Code of Conduct

Please note that this project is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please report it by opening an issue on GitHub. When reporting bugs, please provide:

- A clear and descriptive title
- A detailed description of the issue
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (Python version, PyGUIzer version, OS)
- Any relevant screenshots or logs

### Suggesting Enhancements

We welcome suggestions for new features or improvements to existing functionality. When suggesting enhancements:

- Open an issue on GitHub with a clear title and description
- Explain the expected behavior and use case
- Include any relevant examples or mockups
- Describe how this enhancement would benefit the project

### Pull Requests

We accept pull requests for bug fixes, feature enhancements, and documentation improvements. Before submitting a pull request:

1. Ensure your changes follow the project's style guide
2. Write tests for any new functionality
3. Update documentation as needed
4. Ensure all tests pass
5. Follow the pull request template

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 16+ (for frontend development)
- npm or yarn (for frontend development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pyguizer.git
   cd pyguizer
   ```

2. Install Python dependencies:
   ```bash
   pip install -e .[dev]
   ```

3. Install frontend dependencies (if working on frontend):
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running Tests

PyGUIzer has comprehensive test suites covering unit tests, integration tests, and regression tests.

**Backend Tests:**
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=pyguizer --cov-report=html --cov-report=term-missing

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m regression    # Regression tests only
pytest -m core          # Core functionality tests
pytest -m api           # API endpoint tests

# Run specific test file
pytest tests/test_introspection_unit.py -v

# Run with verbose output and stop on first failure
pytest -v -x

# View HTML coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

**Frontend Tests:**
```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Watch mode for development
npm run test:watch

# Run specific test file
npm test -- App.test.tsx
```

**Test Structure:**
- **Unit Tests**: Test individual modules (`test_*_unit.py`)
- **Integration Tests**: Test complete workflows (`test_api_integration.py`)
- **Regression Tests**: Ensure backward compatibility (`test_regression.py`)
- **Frontend Tests**: Component and integration tests

For more details, see [TESTING.md](TESTING.md) and [tests/README.md](tests/README.md).

### Code Quality

```bash
# Format code with black
black pyguizer/

# Sort imports with isort
isort pyguizer/

# Check with flake8
flake8 pyguizer/

# Run all checks at once
black pyguizer/ && isort pyguizer/ && flake8 pyguizer/
```

## Project Structure

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

## Development Workflow

### Branching Strategy

- `main`: Main development branch
- `feature/`: Feature branches (e.g., `feature/new-widget-type`)
- `bugfix/`: Bug fix branches (e.g., `bugfix/fix-api-routing`)
- `docs/`: Documentation improvement branches

### Commit Messages

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) format for commit messages:

```
<type>: <description>

[optional body]

[optional footer(s)]
```

Common types include:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

### Pull Request Process

1. Fork the repository
2. Create a new branch from `main`
3. Make your changes
4. Write tests for your changes
5. Ensure all tests pass
6. Update documentation as needed
7. Submit a pull request to the `main` branch
8. Wait for code review and address any feedback
9. Once approved, your PR will be merged

## Style Guide

### Python

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Limit line length to 88 characters

### Type Hints

- Use type hints for all function signatures and public APIs
- Follow [PEP 484](https://peps.python.org/pep-0484/) for type annotations
- Use [pydantic](https://pydantic-docs.helpmanual.io/) for data validation

### Documentation

- Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#381-docstrings)
- Document all public functions, classes, and modules
- Update README.md and other documentation as needed

## Testing

PyGUIzer maintains comprehensive test coverage. When contributing:

### Test Requirements

1. **Write tests for new features**: All new functionality must include tests
2. **Update tests for changes**: When modifying existing code, update relevant tests
3. **Test edge cases**: Include tests for error conditions and boundary cases
4. **Maintain coverage**: Aim for 80%+ coverage, 100% for critical paths

### Test Categories

- **Unit Tests** (`-m unit`): Test individual functions and modules
- **Integration Tests** (`-m integration`): Test complete workflows and API endpoints
- **Regression Tests** (`-m regression`): Ensure backward compatibility

### Test Files

**Backend:**
- `test_introspection_unit.py` - Function introspection tests
- `test_widget_unit.py` - Widget generation tests
- `test_layout_unit.py` - Layout processing tests
- `test_api_integration.py` - API endpoint integration tests
- `test_regression.py` - Regression tests

**Frontend:**
- `App.test.tsx` - Main App component tests
- `App.integration.test.tsx` - Integration tests
- `WidgetFactory.test.tsx` - Widget factory tests
- `api.test.ts` - API service tests

### Running Tests Before Submitting

```bash
# Backend: Ensure all tests pass
pytest --cov=pyguizer --cov-fail-under=80

# Frontend: Ensure all tests pass
cd frontend && npm test -- --coverage --watchAll=false
```

See [TESTING.md](TESTING.md) for detailed testing guidelines.

## License

By contributing to PyGUIzer, you agree that your contributions will be licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Thank You!

We appreciate your interest in contributing to PyGUIzer. Your contributions help make PyGUIzer a better tool for everyone!
