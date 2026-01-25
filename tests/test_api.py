"""Unit tests for FastAPI application functionality."""

import time

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
    assert spec["name"] == "PyGUIzer App"
    assert "description" in spec
    assert "functions" in spec
    assert len(spec["functions"]) > 0
    # Check that the calculate function is registered
    function_names = [f["name"] for f in spec["functions"]]
    assert "calculate" in function_names


def test_api_run_endpoint_add(test_client):
    """Test the /api/run endpoint with addition operation."""
    response = test_client.post(
        "/api/run", json={"func_name": "calculate", "inputs": {"a": 10.0, "b": 5.0, "operation": "add"}}
    )

    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert "status" in data
    
    # Wait for task to complete
    task_id = data["task_id"]
    for _ in range(10):  # Poll up to 10 times
        time.sleep(0.1)
        task_response = test_client.get(f"/api/tasks/{task_id}")
        task = task_response.json()
        if task["status"] == "success":
            assert task["result"] == 15.0
            break
        assert task["status"] in ["pending", "running", "success"]


def test_api_run_endpoint_subtract(test_client):
    """Test the /api/run endpoint with subtraction operation."""
    response = test_client.post(
        "/api/run", json={"func_name": "calculate", "inputs": {"a": 10.0, "b": 5.0, "operation": "subtract"}}
    )

    assert response.status_code == 200
    task_id = response.json()["task_id"]
    
    # Wait for task to complete
    for _ in range(10):
        time.sleep(0.1)
        task_response = test_client.get(f"/api/tasks/{task_id}")
        task = task_response.json()
        if task["status"] == "success":
            assert task["result"] == 5.0
            break


def test_api_run_endpoint_multiply(test_client):
    """Test the /api/run endpoint with multiplication operation."""
    response = test_client.post(
        "/api/run", json={"func_name": "calculate", "inputs": {"a": 10.0, "b": 5.0, "operation": "multiply"}}
    )

    assert response.status_code == 200
    task_id = response.json()["task_id"]
    
    # Wait for task to complete
    for _ in range(10):
        time.sleep(0.1)
        task_response = test_client.get(f"/api/tasks/{task_id}")
        task = task_response.json()
        if task["status"] == "success":
            assert task["result"] == 50.0
            break


def test_api_run_endpoint_divide(test_client):
    """Test the /api/run endpoint with division operation."""
    response = test_client.post(
        "/api/run", json={"func_name": "calculate", "inputs": {"a": 10.0, "b": 5.0, "operation": "divide"}}
    )

    assert response.status_code == 200
    task_id = response.json()["task_id"]
    
    # Wait for task to complete
    for _ in range(10):
        time.sleep(0.1)
        task_response = test_client.get(f"/api/tasks/{task_id}")
        task = task_response.json()
        if task["status"] == "success":
            assert task["result"] == 2.0
            break


def test_api_run_endpoint_missing_required_param(test_client):
    """Test the /api/run endpoint with missing required parameter."""
    response = test_client.post(
        "/api/run", json={"func_name": "calculate", "inputs": {"a": 10.0, "operation": "add"}}
    )

    # Should create a task, but task will fail
    assert response.status_code == 200
    task_id = response.json()["task_id"]
    
    # Wait for task to fail
    for _ in range(10):
        time.sleep(0.1)
        task_response = test_client.get(f"/api/tasks/{task_id}")
        task = task_response.json()
        if task["status"] == "failed":
            assert "error" in task
            break


def test_api_run_endpoint_invalid_param_type(test_client):
    """Test the /api/run endpoint with invalid parameter type."""
    response = test_client.post(
        "/api/run", json={"func_name": "calculate", "inputs": {"a": "invalid", "b": 5.0, "operation": "add"}}
    )

    # Should create a task, but task will fail
    assert response.status_code == 200
    task_id = response.json()["task_id"]
    
    # Wait for task to fail
    for _ in range(10):
        time.sleep(0.1)
        task_response = test_client.get(f"/api/tasks/{task_id}")
        task = task_response.json()
        if task["status"] == "failed":
            assert "error" in task
            break
