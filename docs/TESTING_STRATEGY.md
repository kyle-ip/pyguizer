# PyGUIzer Testing Guide

## Overview

PyGUIzer has comprehensive test coverage including:
- **Unit Tests**: Test individual modules and functions
- **Integration Tests**: Test complete workflows and API endpoints
- **Regression Tests**: Ensure backward compatibility and prevent regressions

## Quick Start

### Backend Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=pyguizer --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### Frontend Tests

```bash
cd frontend

# Install dependencies
npm install

# Run tests
npm test

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

## Test Organization

### Backend Test Files

| File | Purpose | Coverage |
|------|---------|----------|
| `test_introspection_unit.py` | Function introspection unit tests | Core module |
| `test_widget_unit.py` | Widget generation unit tests | Core module |
| `test_layout_unit.py` | Layout processing unit tests | Core module |
| `test_api_integration.py` | API endpoint integration tests | API layer |
| `test_multi_function.py` | Multi-function support tests | Feature |
| `test_regression.py` | Regression tests | All modules |

### Frontend Test Files

| File | Purpose | Coverage |
|------|---------|----------|
| `App.test.tsx` | Main App component unit tests | Component |
| `App.integration.test.tsx` | App integration tests | User flows |
| `WidgetFactory.test.tsx` | Widget factory unit tests | Component |
| `api.test.ts` | API service unit tests | Service layer |

## Test Categories

### Unit Tests (`-m unit`)

Test individual functions and modules in isolation:
- Function introspection
- Widget generation
- Layout processing
- Component rendering
- Service functions

**Example:**
```bash
pytest -m unit
```

### Integration Tests (`-m integration`)

Test complete workflows:
- API endpoint flows
- Multi-function execution
- User interaction flows
- End-to-end scenarios

**Example:**
```bash
pytest -m integration
```

### Regression Tests (`-m regression`)

Ensure backward compatibility:
- Core functionality still works
- API contracts unchanged
- Type mappings preserved
- Backward compatibility maintained

**Example:**
```bash
pytest -m regression
```

## Coverage Goals

### Current Coverage

- **Backend Core Modules**: 85%+
- **API Endpoints**: 90%+
- **Frontend Components**: 80%+
- **Frontend Services**: 85%+

### Target Coverage

- **Overall**: 80% minimum
- **Critical Paths**: 100%
- **New Code**: 90% minimum

## Running Specific Tests

### By Module

```bash
# Test introspection only
pytest tests/test_introspection_unit.py

# Test widget generation only
pytest tests/test_widget_unit.py

# Test layout processing only
pytest tests/test_layout_unit.py
```

### By Function

```bash
# Test specific test function
pytest tests/test_introspection_unit.py::TestIntrospectionBasic::test_simple_function
```

### By Marker

```bash
# Core functionality tests
pytest -m core

# API tests
pytest -m api

# Integration tests
pytest -m integration
```

## Test Best Practices

### Writing Backend Tests

1. **Use descriptive test names**: `test_function_name_behavior`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **Test edge cases**: Empty inputs, None values, invalid data
4. **Use fixtures**: Share common test data
5. **Mock external dependencies**: Don't test third-party code

**Example:**
```python
def test_widget_generation_with_defaults(self):
    """Test widget generation includes default values."""
    # Arrange
    params = [{"name": "age", "type": int, "default": 25, ...}]
    
    # Act
    wsos = generate_wso(params)
    
    # Assert
    assert wsos[0]["default"] == 25
```

### Writing Frontend Tests

1. **Test user interactions**: Click, type, submit
2. **Test rendering**: Elements appear correctly
3. **Test state changes**: Component updates properly
4. **Test error handling**: Errors display correctly
5. **Use React Testing Library**: Focus on user behavior

**Example:**
```typescript
it('should update input value when user types', () => {
  render(<Component />);
  const input = screen.getByLabelText('Name');
  fireEvent.change(input, { target: { value: 'John' } });
  expect(input).toHaveValue('John');
});
```

## Continuous Integration

Tests run automatically on:
- Every push to main branch
- Every pull request
- Scheduled nightly runs

### CI Pipeline

The enhanced CI/CD pipeline includes:

1. **Security Scanning**:
   - Bandit: Python code vulnerability scanning
   - pip-audit: Python dependency vulnerability scanning and auto-fix
   - npm audit: Frontend dependency vulnerability scanning and auto-fix
   - Weekly scheduled vulnerability scans

2. **Code Quality & Refactoring**:
   - Automatic fixes: black, isort, autoflake, ESLint
   - PyLint: Code quality analysis with configurable thresholds
   - Auto-commit: Code quality fixes automatically committed to PR branches

3. **Lint**: Code style checks (flake8, black, isort)

4. **Unit Tests**: Fast unit tests across Python 3.8-3.12

5. **Integration Tests**: Complete workflow and API endpoint tests

6. **Regression Tests**: Backward compatibility verification

7. **Frontend Tests**: Unit and integration tests for React components

8. **Coverage**: Generate coverage reports and upload to Codecov

9. **Deployment**: 
   - GitHub Pages: Auto-deploy demos on merge to main
   - PyPI: Auto-publish on merge to main (if configured)

## Debugging Tests

### Backend

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Debug with pdb
pytest --pdb
```

### Frontend

```bash
# Watch mode
npm run test:watch

# Update snapshots
npm test -- -u

# Run specific test
npm test -- App.test.tsx
```

## Common Issues

### Import Errors

**Problem**: `ModuleNotFoundError` or import errors

**Solution**: 
- Ensure you're in the project root
- Run `pip install -e .` for backend
- Run `npm install` for frontend

### Coverage Not Working

**Problem**: Coverage report not generated

**Solution**:
- Install pytest-cov: `pip install pytest-cov`
- Check pytest.ini configuration
- Ensure source paths are correct

### Tests Hanging

**Problem**: Tests never complete

**Solution**:
- Check for infinite loops
- Verify mocks are properly configured
- Check for unclosed connections

## Test Maintenance

### Adding New Tests

1. Create test file following naming convention
2. Add appropriate markers
3. Write comprehensive test cases
4. Ensure coverage meets targets
5. Update this documentation

### Updating Tests

1. Update tests when functionality changes
2. Keep tests in sync with code
3. Remove obsolete tests
4. Refactor for clarity

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
