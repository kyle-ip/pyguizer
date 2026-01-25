"""Comprehensive integration tests for API endpoints."""

import pytest
import time
from fastapi.testclient import TestClient
from pyguizer.api.app import create_app, PyGUIzerApp


@pytest.fixture
def sample_functions():
    """Fixture providing sample functions for testing."""
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
    
    def multiply(x: float, y: float) -> float:
        """Multiply two numbers."""
        return x * y
    
    def greet(name: str, age: int = 25) -> str:
        """Greet a person."""
        return f"Hello {name}, you are {age} years old!"
    
    return [add, multiply, greet]


@pytest.fixture
def pyguizer_app(sample_functions):
    """Fixture providing a PyGUIzerApp instance with registered functions."""
    app = PyGUIzerApp()
    for func in sample_functions:
        app.register_function(func)
    return app


@pytest.fixture
def test_client(pyguizer_app):
    """Fixture providing a FastAPI test client."""
    app = create_app(pyguizer_app=pyguizer_app)
    return TestClient(app)


@pytest.mark.integration
class TestAPISpecEndpoint:
    """Test /api/spec endpoint."""
    
    def test_get_spec(self, test_client):
        """Test getting application specification."""
        response = test_client.get("/api/spec")
        assert response.status_code == 200
        
        spec = response.json()
        assert "name" in spec
        assert "description" in spec
        assert "functions" in spec
        assert len(spec["functions"]) == 3
    
    def test_spec_contains_function_details(self, test_client):
        """Test that spec contains detailed function information."""
        response = test_client.get("/api/spec")
        spec = response.json()
        
        function_names = [f["name"] for f in spec["functions"]]
        assert "add" in function_names
        assert "multiply" in function_names
        assert "greet" in function_names
        
        # Check that each function has required fields
        for func in spec["functions"]:
            assert "name" in func
            assert "display_name" in func
            assert "description" in func
            assert "layout" in func


@pytest.mark.integration
class TestAPIFunctionsEndpoint:
    """Test /api/functions endpoints."""
    
    def test_get_all_functions(self, test_client):
        """Test getting all registered functions."""
        response = test_client.get("/api/functions")
        assert response.status_code == 200
        
        functions = response.json()
        assert len(functions) == 3
        assert all("name" in f for f in functions)
        assert all("display_name" in f for f in functions)
        assert all("description" in f for f in functions)
    
    def test_get_specific_function(self, test_client):
        """Test getting a specific function."""
        response = test_client.get("/api/functions/add")
        assert response.status_code == 200
        
        func = response.json()
        assert func["name"] == "add"
        assert "parameters" in func
        assert "outputs" in func
        assert "layout" in func
    
    def test_get_nonexistent_function(self, test_client):
        """Test getting a non-existent function returns 404."""
        response = test_client.get("/api/functions/nonexistent")
        assert response.status_code == 404


@pytest.mark.integration
class TestAPIRunEndpoint:
    """Test /api/run endpoint."""
    
    def test_run_function_success(self, test_client):
        """Test successfully running a function."""
        response = test_client.post("/api/run", json={
            "func_name": "add",
            "inputs": {"a": 5, "b": 3}
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert "status" in data
        assert data["status"] == "pending"
    
    def test_run_function_with_defaults(self, test_client):
        """Test running a function with default parameters."""
        response = test_client.post("/api/run", json={
            "func_name": "greet",
            "inputs": {"name": "Alice"}
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
    
    def test_run_nonexistent_function(self, test_client):
        """Test running a non-existent function."""
        response = test_client.post("/api/run", json={
            "func_name": "nonexistent",
            "inputs": {}
        })
        
        assert response.status_code == 404
    
    def test_run_function_with_invalid_inputs(self, test_client):
        """Test running a function with invalid inputs."""
        response = test_client.post("/api/run", json={
            "func_name": "add",
            "inputs": {"a": "invalid", "b": 3}
        })
        
        # Should either return 400 or 500 depending on validation
        assert response.status_code in [400, 422, 500]


@pytest.mark.integration
class TestAPITaskEndpoint:
    """Test /api/tasks endpoints."""
    
    def test_get_task_status(self, test_client):
        """Test getting task status."""
        # First create a task
        run_response = test_client.post("/api/run", json={
            "func_name": "add",
            "inputs": {"a": 5, "b": 3}
        })
        task_id = run_response.json()["task_id"]
        
        # Wait a bit for task to start
        time.sleep(0.1)
        
        # Get task status
        response = test_client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        
        task = response.json()
        assert task["task_id"] == task_id
        assert "status" in task
        assert task["status"] in ["pending", "running", "success"]
    
    def test_get_nonexistent_task(self, test_client):
        """Test getting non-existent task."""
        response = test_client.get("/api/tasks/nonexistent")
        assert response.status_code == 404
    
    def test_cancel_task(self, test_client):
        """Test canceling a task."""
        # Create a task
        run_response = test_client.post("/api/run", json={
            "func_name": "add",
            "inputs": {"a": 5, "b": 3}
        })
        task_id = run_response.json()["task_id"]
        
        # Cancel the task
        response = test_client.post(f"/api/tasks/{task_id}/cancel")
        assert response.status_code == 200
        
        # Verify task is cancelled
        task_response = test_client.get(f"/api/tasks/{task_id}")
        task = task_response.json()
        assert task["status"] == "cancelled"


@pytest.mark.integration
class TestAPIPresetsEndpoint:
    """Test /api/presets endpoints."""
    
    def test_create_preset(self, test_client):
        """Test creating a preset."""
        response = test_client.post("/api/presets", json={
            "name": "Test Preset",
            "description": "Test description",
            "values": {"a": 10, "b": 20}
        })
        
        assert response.status_code == 200
        preset = response.json()
        assert preset["name"] == "Test Preset"
        assert preset["description"] == "Test description"
        assert preset["values"] == {"a": 10, "b": 20}
        assert "id" in preset
        assert "created_at" in preset
    
    def test_get_all_presets(self, test_client):
        """Test getting all presets."""
        # Create a preset first
        test_client.post("/api/presets", json={
            "name": "Test Preset",
            "values": {"a": 10}
        })
        
        response = test_client.get("/api/presets")
        assert response.status_code == 200
        presets = response.json()
        assert isinstance(presets, list)
        assert len(presets) > 0
    
    def test_get_specific_preset(self, test_client):
        """Test getting a specific preset."""
        # Create a preset
        create_response = test_client.post("/api/presets", json={
            "name": "Test Preset",
            "values": {"a": 10}
        })
        preset_id = create_response.json()["id"]
        
        # Get the preset
        response = test_client.get(f"/api/presets/{preset_id}")
        assert response.status_code == 200
        preset = response.json()
        assert preset["id"] == preset_id
        assert preset["name"] == "Test Preset"
    
    def test_update_preset(self, test_client):
        """Test updating a preset."""
        # Create a preset
        create_response = test_client.post("/api/presets", json={
            "name": "Test Preset",
            "values": {"a": 10}
        })
        preset_id = create_response.json()["id"]
        
        # Update the preset
        response = test_client.put(f"/api/presets/{preset_id}", json={
            "name": "Updated Preset",
            "values": {"a": 20}
        })
        assert response.status_code == 200
        preset = response.json()
        assert preset["name"] == "Updated Preset"
        assert preset["values"] == {"a": 20}
    
    def test_delete_preset(self, test_client):
        """Test deleting a preset."""
        # Create a preset
        create_response = test_client.post("/api/presets", json={
            "name": "Test Preset",
            "values": {"a": 10}
        })
        preset_id = create_response.json()["id"]
        
        # Delete the preset
        response = test_client.delete(f"/api/presets/{preset_id}")
        assert response.status_code == 200
        
        # Verify it's deleted
        get_response = test_client.get(f"/api/presets/{preset_id}")
        assert get_response.status_code == 404


@pytest.mark.integration
class TestAPIMultiFunction:
    """Test multi-function support."""
    
    def test_multiple_functions_in_spec(self, test_client):
        """Test that spec includes all registered functions."""
        response = test_client.get("/api/spec")
        spec = response.json()
        
        assert len(spec["functions"]) == 3
        function_names = [f["name"] for f in spec["functions"]]
        assert "add" in function_names
        assert "multiply" in function_names
        assert "greet" in function_names
    
    def test_run_different_functions(self, test_client):
        """Test running different functions."""
        # Run add function
        add_response = test_client.post("/api/run", json={
            "func_name": "add",
            "inputs": {"a": 5, "b": 3}
        })
        assert add_response.status_code == 200
        
        # Run multiply function
        mult_response = test_client.post("/api/run", json={
            "func_name": "multiply",
            "inputs": {"x": 2.5, "y": 4.0}
        })
        assert mult_response.status_code == 200
        
        # Run greet function
        greet_response = test_client.post("/api/run", json={
            "func_name": "greet",
            "inputs": {"name": "Bob", "age": 30}
        })
        assert greet_response.status_code == 200


@pytest.mark.integration
class TestAPIErrorHandling:
    """Test API error handling."""
    
    def test_invalid_json(self, test_client):
        """Test handling invalid JSON."""
        response = test_client.post(
            "/api/run",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, test_client):
        """Test handling missing required fields."""
        response = test_client.post("/api/run", json={
            "inputs": {"a": 5}
        })
        assert response.status_code == 422
    
    def test_invalid_endpoint(self, test_client):
        """Test accessing invalid endpoint."""
        response = test_client.get("/api/invalid")
        assert response.status_code == 404
