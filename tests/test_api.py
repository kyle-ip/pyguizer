"""Unit tests for FastAPI application functionality."""

import pytest
from fastapi.testclient import TestClient

from pyguizer.api.app import create_app


@pytest.fixture
def sample_function():
    """Fixture providing a sample function for testing."""

    def calculate(a: float, b: float, operation: str = "add") -> float:
        """Calculate the result of an operation on two numbers."""
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            return a / b
        else:
            return 0.0

    return calculate


@pytest.fixture
def test_client(sample_function):
    """Fixture providing a FastAPI test client."""
    app = create_app(sample_function)
    return TestClient(app)


def test_api_spec_endpoint(test_client):
    """Test the /api/spec endpoint."""
    response = test_client.get("/api/spec")
    assert response.status_code == 200

    spec = response.json()
    assert "name" in spec
    assert spec["name"] == "calculate"
    assert "description" in spec
    assert "sections" in spec
    assert len(spec["sections"]) > 0


def test_api_run_endpoint_add(test_client):
    """Test the /api/run endpoint with addition operation."""
    response = test_client.post(
        "/api/run", json={"inputs": {"a": 10.0, "b": 5.0, "operation": "add"}}
    )

    assert response.status_code == 200
    result = response.json()
    assert "result" in result
    assert result["result"] == 15.0
    assert "execution_time" in result
    assert result["execution_time"] >= 0


def test_api_run_endpoint_subtract(test_client):
    """Test the /api/run endpoint with subtraction operation."""
    response = test_client.post(
        "/api/run", json={"inputs": {"a": 10.0, "b": 5.0, "operation": "subtract"}}
    )

    assert response.status_code == 200
    result = response.json()
    assert result["result"] == 5.0


def test_api_run_endpoint_multiply(test_client):
    """Test the /api/run endpoint with multiplication operation."""
    response = test_client.post(
        "/api/run", json={"inputs": {"a": 10.0, "b": 5.0, "operation": "multiply"}}
    )

    assert response.status_code == 200
    result = response.json()
    assert result["result"] == 50.0


def test_api_run_endpoint_divide(test_client):
    """Test the /api/run endpoint with division operation."""
    response = test_client.post(
        "/api/run", json={"inputs": {"a": 10.0, "b": 5.0, "operation": "divide"}}
    )

    assert response.status_code == 200
    result = response.json()
    assert result["result"] == 2.0


def test_api_run_endpoint_missing_required_param(test_client):
    """Test the /api/run endpoint with missing required parameter."""
    response = test_client.post(
        "/api/run", json={"inputs": {"a": 10.0, "operation": "add"}}
    )

    assert response.status_code == 500


def test_api_run_endpoint_invalid_param_type(test_client):
    """Test the /api/run endpoint with invalid parameter type."""
    response = test_client.post(
        "/api/run", json={"inputs": {"a": "invalid", "b": 5.0, "operation": "add"}}
    )

    assert response.status_code == 500
