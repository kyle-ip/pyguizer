#!/usr/bin/env python3
"""
Test script to verify multi-function support in PyGUIzer
"""

from pyguizer.api.app import PyGUIzerApp

# Define test functions


def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b


# Create a PyGUIzerApp instance and register functions
print("=== Testing PyGUIzer Multi-Function Support ===")

# Create app instance
app = PyGUIzerApp()
print("✓ Created PyGUIzerApp instance")

# Register functions
app.register_function(add)
app.register_function(multiply)
app.register_function(subtract)
print("✓ Registered 3 test functions")

# Get app spec
app_spec = app.get_app_spec()
print(f"✓ Got app spec with {len(app_spec['functions'])} functions")

# Print function details
for func in app_spec["functions"]:
    print(f"  - {func['name']}: {func['display_name']}")

# Test running a function
print("\n=== Testing Function Execution ===")
result = app.run_function("add", {"a": 5, "b": 3})
print(f"✓ Ran add(5, 3) = {result}")
assert result == 8, f"Expected 8, got {result}"

result = app.run_function("multiply", {"a": 5, "b": 3})
print(f"✓ Ran multiply(5, 3) = {result}")
assert result == 15, f"Expected 15, got {result}"

result = app.run_function("subtract", {"a": 5, "b": 3})
print(f"✓ Ran subtract(5, 3) = {result}")
assert result == 2, f"Expected 2, got {result}"

print("\n=== All Tests Passed! ===")
