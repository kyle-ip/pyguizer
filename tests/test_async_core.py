import asyncio
import os
import sys
import time
from typing import List

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing PyGUIzer async core functionality...")

# Test that we can import the PyGUIzer decorator
try:
    from pyguizer import PyGUIzer

    print("✓ Successfully imported PyGUIzer decorator")
except Exception as e:
    print(f"✗ Failed to import PyGUIzer decorator: {e}")
    sys.exit(1)

# Test that we can create both sync and async decorated functions
print("\nTesting function creation...")

try:
    # Create a sync function
    @PyGUIzer()
    def sync_function(x: int, y: int) -> int:
        """Sync function that sleeps to simulate work."""
        time.sleep(0.1)  # Simulate blocking work
        return x + y

    print("✓ Successfully created sync function")
except Exception as e:
    print(f"✗ Failed to create sync function: {e}")
    sys.exit(1)

try:
    # Create an async function
    @PyGUIzer()
    async def async_function(x: int, y: int) -> int:
        """Async function that sleeps to simulate work."""
        await asyncio.sleep(0.1)  # Simulate non-blocking work
        return x * y

    print("✓ Successfully created async function")
except Exception as e:
    print(f"✗ Failed to create async function: {e}")
    sys.exit(1)

try:
    # Create another async function with complex return type
    @PyGUIzer()
    async def async_data_processor(data: List[int]) -> dict:
        """Async function that processes a list of data."""
        await asyncio.sleep(0.05)  # Simulate work
        return {
            "sum": sum(data),
            "average": sum(data) / len(data) if data else 0,
            "max": max(data) if data else 0,
            "min": min(data) if data else 0,
        }

    print("✓ Successfully created async function with complex return type")
except Exception as e:
    print(f"✗ Failed to create async function with complex return type: {e}")
    sys.exit(1)

# Test that the decorator adds the __pyguizer__ attribute
try:
    assert hasattr(
        sync_function, "__pyguizer__"
    ), "Sync function should have __pyguizer__ attribute"
    assert hasattr(
        async_function, "__pyguizer__"
    ), "Async function should have __pyguizer__ attribute"
    print(
        "✓ Decorator correctly adds __pyguizer__ attribute to both sync and async functions"
    )
except AssertionError as e:
    print(f"✗ {e}")
    sys.exit(1)

# Test that we can access the PyGUIzer instance
try:
    sync_instance = sync_function.__pyguizer__
    async_instance = async_function.__pyguizer__
    assert hasattr(
        sync_instance, "func"
    ), "PyGUIzer instance should have func attribute"
    assert hasattr(
        async_instance, "func"
    ), "PyGUIzer instance should have func attribute"
    print("✓ Can access PyGUIzer instance for both sync and async functions")
except Exception as e:
    print(f"✗ Failed to access PyGUIzer instance: {e}")
    sys.exit(1)

# Test function introspection
try:
    from pyguizer.core.introspection import introspect_function

    sync_info = introspect_function(sync_function)
    async_info = introspect_function(async_function)

    assert sync_info["name"] == "sync_function", "Sync function name should be correct"
    assert (
        async_info["name"] == "async_function"
    ), "Async function name should be correct"
    assert len(sync_info["parameters"]) == 2, "Sync function should have 2 parameters"
    assert len(async_info["parameters"]) == 2, "Async function should have 2 parameters"

    print("✓ Function introspection works for both sync and async functions")
except Exception as e:
    print(f"✗ Failed function introspection: {e}")
    sys.exit(1)

# Test widget generation
try:
    from pyguizer.core.widget import generate_wso

    sync_info = introspect_function(sync_function)
    async_info = introspect_function(async_function)

    sync_wsos = generate_wso(sync_info["parameters"])
    async_wsos = generate_wso(async_info["parameters"])

    assert len(sync_wsos) == 2, "Sync function should generate 2 widgets"
    assert len(async_wsos) == 2, "Async function should generate 2 widgets"

    print("✓ Widget generation works for both sync and async functions")
except Exception as e:
    print(f"✗ Failed widget generation: {e}")
    sys.exit(1)

# Test async function execution
try:
    import asyncio

    async def test_async_execution():
        """Test async execution of both sync and async functions."""
        # Create a PyGUIzerApp instance
        from pyguizer.api.app import PyGUIzerApp

        app = PyGUIzerApp()
        app.register_function(sync_function)
        app.register_function(async_function)
        app.register_function(async_data_processor)

        # Test sync function
        sync_result = await app.run_function("sync_function", {"x": 10, "y": 20})
        assert sync_result == 30, f"Sync function should return 30, got {sync_result}"

        # Test async function
        async_result = await app.run_function("async_function", {"x": 5, "y": 6})
        assert (
            async_result == 30
        ), f"Async function should return 30, got {async_result}"

        # Test async function with complex return type
        data_result = await app.run_function(
            "async_data_processor", {"data": [1, 2, 3, 4, 5]}
        )
        assert (
            data_result["sum"] == 15
        ), f"Async data processor should return sum 15, got {data_result['sum']}"

        return True

    # Run the async test
    success = asyncio.run(test_async_execution())
    if success:
        print("✓ Async function execution works for both sync and async functions")
    else:
        print("✗ Async function execution failed")
        sys.exit(1)
except Exception as e:
    print(f"✗ Failed async function execution: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n🎉 All async core functionality tests passed!")
print("PyGUIzer async support is working correctly.")
