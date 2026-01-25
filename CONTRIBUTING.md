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

```bash
# Run all tests
python -m pytest

# Run specific test modules
python -m pytest tests/test_core.py -v
python -m pytest tests/verify_core.py -v

# Run tests with coverage
python -m pytest --cov=pyguizer
```

### Code Quality

```bash
# Format code with black
black pyguizer/ tests/ examples/

# Sort imports with isort
isort pyguizer/ tests/ examples/

# Check with flake8
flake8 pyguizer/ tests/

# Remove unused imports and variables with autoflake
autoflake --remove-all-unused-imports --remove-unused-variables --in-place -r pyguizer/ tests/ examples/

# Run PyLint for code quality analysis
pylint pyguizer/ tests/ examples/

# Run all checks at once
black pyguizer/ tests/ examples/ && isort pyguizer/ tests/ examples/ && flake8 pyguizer/ tests/
```

**Note**: The CI/CD pipeline automatically runs these tools and fixes issues when you create a pull request. Code quality fixes are automatically committed back to your PR branch.

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
5. Ensure all tests pass locally
6. Update documentation as needed
7. Submit a pull request to the `main` branch
8. **CI/CD Pipeline**: The automated pipeline will:
   - Scan for security vulnerabilities (Bandit, pip-audit, npm audit)
   - Automatically fix code quality issues (black, isort, autoflake, ESLint)
   - Run PyLint for code quality analysis
   - Run unit, integration, and regression tests across Python 3.8-3.12
   - Run frontend unit and integration tests
   - Build the frontend and Python package
   - Auto-commit code quality fixes to your PR branch
9. Wait for code review and address any feedback
10. Once approved, your PR will be merged
11. On merge to `main`, the pipeline will:
    - Deploy the demo to GitHub Pages (including examples)
    - Publish to PyPI (if configured)

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

- Write unit tests for core functionality
- Write integration tests for API endpoints
- Test edge cases and error conditions
- Aim for high test coverage (target: 80%+)

### CI/CD Testing

The CI/CD pipeline automatically runs:
- **Unit tests**: Fast, isolated tests for individual components
- **Integration tests**: Tests for complete workflows and API endpoints
- **Regression tests**: Ensures backward compatibility
- **Frontend tests**: Unit and integration tests for React components
- **Multi-version testing**: Tests run on Python 3.8, 3.9, 3.10, 3.11, and 3.12

All tests must pass before a PR can be merged. Coverage reports are uploaded to Codecov.

## License

By contributing to PyGUIzer, you agree that your contributions will be licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Thank You!

We appreciate your interest in contributing to PyGUIzer. Your contributions help make PyGUIzer a better tool for everyone!
