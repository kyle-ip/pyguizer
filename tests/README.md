# PyGUIzer Test Suite

This directory contains comprehensive test suites for PyGUIzer, including unit tests, integration tests, and regression tests.

## Test Structure

### Backend Tests

#### Unit Tests
- `test_introspection_unit.py` - Unit tests for function introspection module
- `test_widget_unit.py` - Unit tests for widget generation module
- `test_layout_unit.py` - Unit tests for layout processing module

#### Integration Tests
- `test_api_integration.py` - Integration tests for all API endpoints
- `test_multi_function.py` - Integration tests for multi-function support

#### Regression Tests
- `test_regression.py` - Regression tests to ensure core functionality continues to work

### Frontend Tests

#### Unit Tests
- `frontend/src/App.test.tsx` - Unit tests for main App component
- `frontend/src/components/WidgetFactory.test.tsx` - Unit tests for WidgetFactory component
- `frontend/src/services/api.test.ts` - Unit tests for API service

#### Integration Tests
- `frontend/src/App.integration.test.tsx` - Integration tests for complete user flows

## Running Tests

### Backend Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=pyguizer --cov-report=html
```

Run specific test categories:
```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Regression tests only
pytest -m regression

# Core functionality tests
pytest -m core

# API tests
pytest -m api
```

Run specific test file:
```bash
pytest tests/test_introspection_unit.py
```

### Frontend Tests

Run all tests:
```bash
cd frontend
npm test
```

Run with coverage:
```bash
cd frontend
npm run test:coverage
```

Run in watch mode:
```bash
cd frontend
npm run test:watch
```

## Test Coverage Goals

- **Backend**: Minimum 80% coverage
- **Frontend**: Minimum 80% coverage
- **Critical Paths**: 100% coverage

## Test Categories

### Unit Tests
Test individual functions and modules in isolation with mocked dependencies.

### Integration Tests
Test complete workflows and API endpoints with real implementations.

### Regression Tests
Ensure that previously working functionality continues to work after changes.

## Writing New Tests

### Backend Test Template

```python
import pytest
from pyguizer.core.module import function_to_test

class TestModuleName:
    """Test description."""
    
    def test_specific_feature(self):
        """Test specific feature."""
        # Arrange
        input_data = ...
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == expected_value
```

### Frontend Test Template

```typescript
import React from 'react';
import { render, screen } from '@testing-library/react';
import Component from './Component';

describe('Component', () => {
  it('should render correctly', () => {
    render(<Component />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
});
```

## Continuous Integration

Tests are automatically run in CI/CD pipeline:
- All tests must pass before merging
- Coverage reports are generated
- Test results are published

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure you're running tests from the project root
2. **Missing dependencies**: Run `pip install -e .[dev]` for backend, `npm install` for frontend
3. **Coverage not working**: Ensure pytest-cov is installed

### Debugging Tests

Run tests with verbose output:
```bash
pytest -v -s
```

Run single test with debugging:
```bash
pytest tests/test_file.py::TestClass::test_method -v -s
```
