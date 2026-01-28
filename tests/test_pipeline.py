"""Test cases for pipeline functionality"""

import asyncio

import pytest
from fastapi.testclient import TestClient

from pyguizer.api.app import create_app


# Test functions
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


def multiply(x: int, y: int) -> int:
    """Multiply two numbers"""
    return x * y


def divide(x: int, y: int) -> float:
    """Divide two numbers"""
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y


def greet(name: str, age: int = 25) -> str:
    """Greet a person with optional age"""
    return f"Hello {name}, you are {age} years old!"


async def async_add(a: int, b: int) -> int:
    """Async add two numbers"""
    await asyncio.sleep(0.1)
    return a + b


async def async_multiply(x: int, y: int) -> int:
    """Async multiply two numbers"""
    await asyncio.sleep(0.1)
    return x * y


async def async_slow_function(value: int) -> int:
    """Slow async function to test parallel execution"""
    await asyncio.sleep(0.3)
    return value * 2


# Fixtures
@pytest.fixture
def pyguizer_app_with_functions():
    """Fixture providing a PyGUIzerApp with registered functions"""
    from pyguizer.api.app import PyGUIzerApp

    app = PyGUIzerApp()
    app.register_function(add)
    app.register_function(multiply)
    app.register_function(divide)
    app.register_function(greet)
    app.register_function(async_add)
    app.register_function(async_multiply)
    app.register_function(async_slow_function)
    return app


@pytest.fixture
def test_client_with_functions(pyguizer_app_with_functions):
    """Fixture providing a test client with registered functions"""
    app = create_app(pyguizer_app_with_functions)
    return TestClient(app)


@pytest.fixture
def test_pipeline(test_client_with_functions):
    """Fixture providing a test pipeline"""
    client = test_client_with_functions
    pipeline_data = {"name": "Test Pipeline", "description": "A test pipeline"}
    response = client.post("/api/pipelines", json=pipeline_data)
    if response.status_code != 200:
        print(f"Response content: {response.json()}")
    assert response.status_code == 200
    return response.json()["id"]


# Basic pipeline tests
def test_pipeline_creation():
    """Test pipeline creation and basic CRUD operations"""
    app = create_app()
    client = TestClient(app)

    # Create a pipeline
    pipeline_data = {"name": "Test Pipeline", "description": "A test pipeline"}

    response = client.post("/api/pipelines", json=pipeline_data)
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.json()}")
    assert response.status_code == 200
    pipeline = response.json()
    assert pipeline["name"] == "Test Pipeline"
    assert pipeline["description"] == "A test pipeline"
    pipeline_id = pipeline["id"]

    # Get all pipelines
    response = client.get("/api/pipelines")
    assert response.status_code == 200
    pipelines = response.json()
    assert len(pipelines) == 1

    # Get specific pipeline
    response = client.get(f"/api/pipelines/{pipeline_id}")
    assert response.status_code == 200
    assert response.json()["id"] == pipeline_id

    # Update pipeline
    update_data = {
        "name": "Updated Test Pipeline",
        "description": "An updated test pipeline",
    }
    response = client.put(f"/api/pipelines/{pipeline_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Test Pipeline"

    # Delete pipeline
    response = client.delete(f"/api/pipelines/{pipeline_id}")
    assert response.status_code == 200

    # Verify deletion
    response = client.get("/api/pipelines")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_pipeline_node_management():
    """Test pipeline node management"""
    app = create_app()
    client = TestClient(app)

    # Register test functions
    from pyguizer.api.app import PyGUIzerApp

    pyguizer_app = PyGUIzerApp()
    pyguizer_app.register_function(add)
    pyguizer_app.register_function(multiply)
    app = create_app(pyguizer_app)
    client = TestClient(app)

    # Create a pipeline
    pipeline_data = {"name": "Test Pipeline", "description": "A test pipeline"}
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add a node
    node_data = {
        "function_name": "add",
        "node_name": "Add Node",
        "parameters": {"a": 1, "b": 2},
        "position": {"x": 100, "y": 100},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["function_name"] == "add"
    assert node["node_name"] == "Add Node"
    node_id = node["id"]

    # Update node
    update_data = {"node_name": "Updated Add Node", "parameters": {"a": 5, "b": 5}}
    response = client.put(
        f"/api/pipelines/{pipeline_id}/nodes/{node_id}", json=update_data
    )
    assert response.status_code == 200
    assert response.json()["node_name"] == "Updated Add Node"
    assert response.json()["parameters"] == {"a": 5, "b": 5}

    # Delete node
    response = client.delete(f"/api/pipelines/{pipeline_id}/nodes/{node_id}")
    assert response.status_code == 200

    # Verify node deletion
    response = client.get(f"/api/pipelines/{pipeline_id}")
    assert response.status_code == 200
    assert len(response.json()["nodes"]) == 0


def test_pipeline_connection_management():
    """Test pipeline connection management"""
    app = create_app()
    client = TestClient(app)

    # Register test functions
    from pyguizer.api.app import PyGUIzerApp

    pyguizer_app = PyGUIzerApp()
    pyguizer_app.register_function(add)
    pyguizer_app.register_function(multiply)
    app = create_app(pyguizer_app)
    client = TestClient(app)

    # Create a pipeline
    pipeline_data = {"name": "Test Pipeline", "description": "A test pipeline"}
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add nodes
    node1_data = {
        "function_name": "add",
        "node_name": "Add Node",
        "parameters": {"a": 1, "b": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node1_data)
    node1_id = response.json()["id"]

    node2_data = {
        "function_name": "multiply",
        "node_name": "Multiply Node",
        "parameters": {"y": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node2_data)
    node2_id = response.json()["id"]

    # Add connection
    connection_data = {
        "source_node_id": node1_id,
        "source_output": "result",
        "target_node_id": node2_id,
        "target_input": "x",
    }
    response = client.post(
        f"/api/pipelines/{pipeline_id}/connections", json=connection_data
    )
    assert response.status_code == 200
    connection = response.json()
    assert connection["source_node_id"] == node1_id
    assert connection["target_node_id"] == node2_id
    connection_id = connection["id"]

    # Verify connection exists
    response = client.get(f"/api/pipelines/{pipeline_id}")
    assert response.status_code == 200
    assert len(response.json()["connections"]) == 1

    # Delete connection
    response = client.delete(
        f"/api/pipelines/{pipeline_id}/connections/{connection_id}"
    )
    assert response.status_code == 200

    # Verify connection deletion
    response = client.get(f"/api/pipelines/{pipeline_id}")
    assert response.status_code == 200
    assert len(response.json()["connections"]) == 0


def test_pipeline_validation():
    """Test pipeline validation and cyclic dependency detection"""
    app = create_app()
    client = TestClient(app)

    # Register test functions
    from pyguizer.api.app import PyGUIzerApp

    pyguizer_app = PyGUIzerApp()
    pyguizer_app.register_function(add)
    pyguizer_app.register_function(multiply)
    app = create_app(pyguizer_app)
    client = TestClient(app)

    # Create a pipeline
    pipeline_data = {"name": "Test Pipeline", "description": "A test pipeline"}
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add nodes
    node1_data = {
        "function_name": "add",
        "node_name": "Add Node",
        "parameters": {"a": 1, "b": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node1_data)
    node1_id = response.json()["id"]

    node2_data = {
        "function_name": "multiply",
        "node_name": "Multiply Node",
        "parameters": {"y": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node2_data)
    node2_id = response.json()["id"]

    # Add connection
    connection_data = {
        "source_node_id": node1_id,
        "source_output": "result",
        "target_node_id": node2_id,
        "target_input": "x",
    }
    response = client.post(
        f"/api/pipelines/{pipeline_id}/connections", json=connection_data
    )
    assert response.status_code == 200

    # Validate pipeline (should pass)
    response = client.post(f"/api/pipelines/{pipeline_id}/validate")
    assert response.status_code == 200
    validation = response.json()
    assert validation["valid"] is True

    # Try to create a cyclic dependency
    # Add a connection from node2 back to node1
    cyclic_connection_data = {
        "source_node_id": node2_id,
        "source_output": "result",
        "target_node_id": node1_id,
        "target_input": "a",
    }
    response = client.post(
        f"/api/pipelines/{pipeline_id}/connections", json=cyclic_connection_data
    )
    assert response.status_code == 400
    assert "cyclic dependency" in response.json()["detail"]


@pytest.mark.asyncio
async def test_pipeline_execution_serial():
    """Test pipeline execution in serial mode"""
    from pyguizer.api.app import PyGUIzerApp

    pyguizer_app = PyGUIzerApp()
    pyguizer_app.register_function(add)
    pyguizer_app.register_function(multiply)
    app = create_app(pyguizer_app)
    client = TestClient(app)

    # Create a pipeline
    pipeline_data = {"name": "Test Pipeline", "description": "A test pipeline"}
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add nodes
    node1_data = {
        "function_name": "add",
        "node_name": "Add Node",
        "parameters": {"a": 1, "b": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node1_data)
    node1_id = response.json()["id"]

    node2_data = {
        "function_name": "multiply",
        "node_name": "Multiply Node",
        "parameters": {"y": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node2_data)
    node2_id = response.json()["id"]

    # Add connection
    connection_data = {
        "source_node_id": node1_id,
        "source_output": "result",
        "target_node_id": node2_id,
        "target_input": "x",
    }
    response = client.post(
        f"/api/pipelines/{pipeline_id}/connections", json=connection_data
    )
    assert response.status_code == 200

    # Execute pipeline in serial mode
    execution_data = {"execution_mode": "serial", "run_async": True}
    response = client.post(f"/api/pipelines/{pipeline_id}/execute", json=execution_data)
    assert response.status_code == 200
    execution_id = response.json()["execution_id"]

    # Get execution status
    import time

    max_wait = 5.0  # Maximum wait time in seconds
    start_time = time.time()

    while time.time() - start_time < max_wait:
        time.sleep(0.1)  # Short wait between checks
        response = client.get(f"/api/tasks/{execution_id}")
        assert response.status_code == 200
        task = response.json()
        if task["status"] in ["success", "failed"]:
            break

    assert task["status"] == "success"
    result = task["result"]
    assert result["status"] == "completed"
    assert "results" in result


@pytest.mark.asyncio
async def test_pipeline_execution_parallel():
    """Test pipeline execution in parallel mode"""
    from pyguizer.api.app import PyGUIzerApp

    pyguizer_app = PyGUIzerApp()
    pyguizer_app.register_function(add)
    pyguizer_app.register_function(multiply)
    pyguizer_app.register_function(async_add)
    pyguizer_app.register_function(async_multiply)
    app = create_app(pyguizer_app)
    client = TestClient(app)

    # Create a pipeline
    pipeline_data = {"name": "Test Pipeline", "description": "A test pipeline"}
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add independent nodes (can run in parallel)
    node1_data = {
        "function_name": "async_add",
        "node_name": "Async Add Node",
        "parameters": {"a": 1, "b": 2},
    }
    client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node1_data)

    node2_data = {
        "function_name": "async_multiply",
        "node_name": "Async Multiply Node",
        "parameters": {"x": 3, "y": 4},
    }
    client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node2_data)

    # Execute pipeline in parallel mode
    execution_data = {"execution_mode": "parallel", "run_async": True}
    response = client.post(f"/api/pipelines/{pipeline_id}/execute", json=execution_data)
    assert response.status_code == 200
    execution_id = response.json()["execution_id"]

    # Get execution status
    import time

    time.sleep(0.5)  # Wait for execution to complete
    response = client.get(f"/api/tasks/{execution_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["status"] == "success"
    result = task["result"]
    assert result["status"] == "completed"
    assert "results" in result


# Edge Case Tests
def test_pipeline_with_no_nodes(test_client_with_functions):
    """Test pipeline with no nodes"""
    client = test_client_with_functions

    # Create a pipeline
    pipeline_data = {
        "name": "Empty Pipeline",
        "description": "A pipeline with no nodes",
    }
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Validate pipeline (should pass)
    response = client.post(f"/api/pipelines/{pipeline_id}/validate")
    assert response.status_code == 200
    validation = response.json()
    assert validation["valid"] is True

    # Execute pipeline (should work)
    execution_data = {"execution_mode": "serial", "run_async": True}
    response = client.post(f"/api/pipelines/{pipeline_id}/execute", json=execution_data)
    assert response.status_code == 200
    execution_id = response.json()["execution_id"]

    # Get execution status
    import time

    max_wait = 5.0  # Maximum wait time in seconds
    start_time = time.time()

    while time.time() - start_time < max_wait:
        time.sleep(0.1)  # Short wait between checks
        response = client.get(f"/api/tasks/{execution_id}")
        assert response.status_code == 200
        task = response.json()
        if task["status"] in ["success", "failed"]:
            break

    assert task["status"] == "success"


def test_pipeline_with_nodes_no_connections(test_client_with_functions):
    """Test pipeline with nodes but no connections"""
    client = test_client_with_functions

    # Create a pipeline
    pipeline_data = {
        "name": "No Connections Pipeline",
        "description": "A pipeline with nodes but no connections",
    }
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add nodes
    node1_data = {
        "function_name": "add",
        "node_name": "Add Node",
        "parameters": {"a": 1, "b": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node1_data)

    node2_data = {
        "function_name": "multiply",
        "node_name": "Multiply Node",
        "parameters": {"x": 3, "y": 4},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node2_data)

    # Validate pipeline (should pass)
    response = client.post(f"/api/pipelines/{pipeline_id}/validate")
    assert response.status_code == 200
    validation = response.json()
    assert validation["valid"] is True

    # Execute pipeline (should work)
    execution_data = {"execution_mode": "parallel", "run_async": True}
    response = client.post(f"/api/pipelines/{pipeline_id}/execute", json=execution_data)
    assert response.status_code == 200
    execution_id = response.json()["execution_id"]

    # Get execution status
    import time

    time.sleep(0.5)
    response = client.get(f"/api/tasks/{execution_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["status"] == "success"


def test_pipeline_with_function_errors(test_client_with_functions):
    """Test pipeline with functions that throw errors"""
    client = test_client_with_functions

    # Create a pipeline
    pipeline_data = {
        "name": "Error Pipeline",
        "description": "A pipeline with functions that throw errors",
    }
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add nodes
    node1_data = {
        "function_name": "add",
        "node_name": "Add Node",
        "parameters": {"a": 10, "b": 5},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node1_data)
    node1_id = response.json()["id"]

    node2_data = {
        "function_name": "divide",
        "node_name": "Divide Node",
        "parameters": {"y": 0},  # This will cause an error
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node2_data)
    node2_id = response.json()["id"]

    # Add connection
    connection_data = {
        "source_node_id": node1_id,
        "source_output": "result",
        "target_node_id": node2_id,
        "target_input": "x",
    }
    response = client.post(
        f"/api/pipelines/{pipeline_id}/connections", json=connection_data
    )
    assert response.status_code == 200

    # Execute pipeline
    execution_data = {"execution_mode": "serial", "run_async": True}
    response = client.post(f"/api/pipelines/{pipeline_id}/execute", json=execution_data)
    assert response.status_code == 200
    execution_id = response.json()["execution_id"]

    # Get execution status
    import time

    time.sleep(0.5)
    response = client.get(f"/api/tasks/{execution_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["status"] == "failed"
    assert "error" in task


def test_pipeline_with_default_parameters(test_client_with_functions):
    """Test pipeline with functions that have default parameters"""
    client = test_client_with_functions

    # Create a pipeline
    pipeline_data = {
        "name": "Default Params Pipeline",
        "description": "A pipeline with functions that have default parameters",
    }
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add node with only required parameter
    node_data = {
        "function_name": "greet",
        "node_name": "Greet Node",
        "parameters": {"name": "Alice"},  # Age should use default
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node_data)
    assert response.status_code == 200

    # Execute pipeline
    execution_data = {"execution_mode": "serial", "run_async": True}
    response = client.post(f"/api/pipelines/{pipeline_id}/execute", json=execution_data)
    assert response.status_code == 200
    execution_id = response.json()["execution_id"]

    # Get execution status
    import time

    time.sleep(0.5)
    response = client.get(f"/api/tasks/{execution_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["status"] == "success"


@pytest.mark.asyncio
async def test_pipeline_complex_dependencies():
    """Test pipeline with complex dependencies"""
    from pyguizer.api.app import PyGUIzerApp

    pyguizer_app = PyGUIzerApp()
    pyguizer_app.register_function(add)
    pyguizer_app.register_function(multiply)
    pyguizer_app.register_function(divide)
    app = create_app(pyguizer_app)
    client = TestClient(app)

    # Create a pipeline
    pipeline_data = {
        "name": "Complex Pipeline",
        "description": "A pipeline with complex dependencies",
    }
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add nodes
    node1_data = {
        "function_name": "add",
        "node_name": "Add 1",
        "parameters": {"a": 1, "b": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node1_data)
    node1_id = response.json()["id"]

    node2_data = {
        "function_name": "add",
        "node_name": "Add 2",
        "parameters": {"a": 3, "b": 4},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node2_data)
    node2_id = response.json()["id"]

    node3_data = {
        "function_name": "multiply",
        "node_name": "Multiply",
        "parameters": {},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node3_data)
    node3_id = response.json()["id"]

    node4_data = {
        "function_name": "divide",
        "node_name": "Divide",
        "parameters": {"y": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node4_data)
    node4_id = response.json()["id"]

    # Add connections
    # node1 -> node3.x
    connection1_data = {
        "source_node_id": node1_id,
        "source_output": "result",
        "target_node_id": node3_id,
        "target_input": "x",
    }
    response = client.post(
        f"/api/pipelines/{pipeline_id}/connections", json=connection1_data
    )
    assert response.status_code == 200

    # node2 -> node3.y
    connection2_data = {
        "source_node_id": node2_id,
        "source_output": "result",
        "target_node_id": node3_id,
        "target_input": "y",
    }
    response = client.post(
        f"/api/pipelines/{pipeline_id}/connections", json=connection2_data
    )
    assert response.status_code == 200

    # node3 -> node4.x
    connection3_data = {
        "source_node_id": node3_id,
        "source_output": "result",
        "target_node_id": node4_id,
        "target_input": "x",
    }
    response = client.post(
        f"/api/pipelines/{pipeline_id}/connections", json=connection3_data
    )
    assert response.status_code == 200

    # Validate pipeline
    response = client.post(f"/api/pipelines/{pipeline_id}/validate")
    assert response.status_code == 200
    validation = response.json()
    assert validation["valid"] is True

    # Execute pipeline
    execution_data = {"execution_mode": "serial", "run_async": True}
    response = client.post(f"/api/pipelines/{pipeline_id}/execute", json=execution_data)
    assert response.status_code == 200
    execution_id = response.json()["execution_id"]

    # Get execution status
    import time

    time.sleep(0.5)
    response = client.get(f"/api/tasks/{execution_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["status"] == "success"


@pytest.mark.asyncio
async def test_pipeline_concurrent_executions():
    """Test concurrent pipeline executions"""
    from pyguizer.api.app import PyGUIzerApp

    pyguizer_app = PyGUIzerApp()
    pyguizer_app.register_function(async_slow_function)
    app = create_app(pyguizer_app)
    client = TestClient(app)

    # Create a pipeline
    pipeline_data = {
        "name": "Concurrent Pipeline",
        "description": "A pipeline for concurrent testing",
    }
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add a slow node
    node_data = {
        "function_name": "async_slow_function",
        "node_name": "Slow Node",
        "parameters": {"value": 10},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node_data)

    # Start multiple executions
    execution_ids = []
    for i in range(3):
        execution_data = {"execution_mode": "serial", "run_async": True}
        response = client.post(
            f"/api/pipelines/{pipeline_id}/execute", json=execution_data
        )
        assert response.status_code == 200
        execution_ids.append(response.json()["execution_id"])

    # Wait for all executions to complete
    import time

    max_wait = 10.0  # Maximum wait time in seconds
    start_time = time.time()

    while time.time() - start_time < max_wait:
        time.sleep(0.1)  # Short wait between checks

        # Check if all executions are complete
        all_completed = True
        for execution_id in execution_ids:
            response = client.get(f"/api/tasks/{execution_id}")
            assert response.status_code == 200
            task = response.json()
            if task["status"] not in ["success", "failed"]:
                all_completed = False
                break

        if all_completed:
            break

    # Check all executions
    for execution_id in execution_ids:
        response = client.get(f"/api/tasks/{execution_id}")
        assert response.status_code == 200
        task = response.json()
        assert task["status"] == "success"


# Error Handling Tests
def test_pipeline_invalid_node_function(test_client_with_functions):
    """Test pipeline with invalid node function"""
    client = test_client_with_functions

    # Create a pipeline
    pipeline_data = {
        "name": "Invalid Function Pipeline",
        "description": "A pipeline with invalid function",
    }
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add node with invalid function
    node_data = {
        "function_name": "nonexistent_function",
        "node_name": "Invalid Node",
        "parameters": {"a": 1, "b": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node_data)
    assert response.status_code == 404
    assert "Function 'nonexistent_function' not found" in response.json()["detail"]


def test_pipeline_invalid_connection(test_client_with_functions):
    """Test pipeline with invalid connection"""
    client = test_client_with_functions

    # Create a pipeline
    pipeline_data = {
        "name": "Invalid Connection Pipeline",
        "description": "A pipeline with invalid connection",
    }
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add a node
    node_data = {
        "function_name": "add",
        "node_name": "Add Node",
        "parameters": {"a": 1, "b": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node_data)
    node_id = response.json()["id"]

    # Add invalid connection (non-existent source node)
    connection_data = {
        "source_node_id": "nonexistent-node",
        "source_output": "result",
        "target_node_id": node_id,
        "target_input": "a",
    }
    response = client.post(
        f"/api/pipelines/{pipeline_id}/connections", json=connection_data
    )
    assert response.status_code == 404
    assert "Source node not found in pipeline" in response.json()["detail"]


def test_pipeline_invalid_target_input(test_client_with_functions):
    """Test pipeline with invalid target input"""
    client = test_client_with_functions

    # Create a pipeline
    pipeline_data = {
        "name": "Invalid Input Pipeline",
        "description": "A pipeline with invalid target input",
    }
    response = client.post("/api/pipelines", json=pipeline_data)
    pipeline_id = response.json()["id"]

    # Add nodes
    node1_data = {
        "function_name": "add",
        "node_name": "Add Node",
        "parameters": {"a": 1, "b": 2},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node1_data)
    node1_id = response.json()["id"]

    node2_data = {
        "function_name": "add",
        "node_name": "Add Node 2",
        "parameters": {"a": 3},
    }
    response = client.post(f"/api/pipelines/{pipeline_id}/nodes", json=node2_data)
    node2_id = response.json()["id"]

    # Add connection with invalid target input
    connection_data = {
        "source_node_id": node1_id,
        "source_output": "result",
        "target_node_id": node2_id,
        "target_input": "nonexistent_input",
    }
    response = client.post(
        f"/api/pipelines/{pipeline_id}/connections", json=connection_data
    )
    assert response.status_code == 400
    assert "Target input 'nonexistent_input' not found" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main([__file__])
