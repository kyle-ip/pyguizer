"""Unit tests for function introspection functionality."""

from pyguizer.core.introspection import introspect_function


def test_introspect_simple_function():
    """Test introspection of a simple function with type hints."""

    def sample_func(name: str, age: int) -> str:
        """Sample function for testing."""
        return f"Hello {name}, you are {age} years old."

    result = introspect_function(sample_func)

    # Verify basic function info
    assert result["name"] == "sample_func"
    assert result["docstring"] == "Sample function for testing."

    # Verify parameters
    assert len(result["parameters"]) == 2

    # Verify first parameter
    param1 = result["parameters"][0]
    assert param1["name"] == "name"
    assert str(param1["type"]).split("'").pop(1) == "str"
    assert param1["required"] is True
    assert param1["default"] is None

    # Verify second parameter
    param2 = result["parameters"][1]
    assert param2["name"] == "age"
    assert str(param2["type"]).split("'").pop(1) == "int"
    assert param2["required"] is True
    assert param2["default"] is None

    # Verify return type
    assert str(result["return_type"]).split("'").pop(1) == "str"


def test_introspect_function_with_defaults():
    """Test introspection of a function with default values."""

    def sample_func(name: str, age: int = 30, active: bool = True) -> dict:
        """Sample function with defaults."""
        return {"name": name, "age": age, "active": active}

    result = introspect_function(sample_func)

    assert len(result["parameters"]) == 3

    # Verify parameter with default
    param2 = result["parameters"][1]
    assert param2["name"] == "age"
    assert param2["default"] == 30
    assert param2["required"] is False

    param3 = result["parameters"][2]
    assert param3["name"] == "active"
    assert param3["default"] is True
    assert param3["required"] is False


def test_introspect_function_without_type_hints():
    """Test introspection of a function without type hints."""

    def sample_func(name, age):
        """Sample function without type hints."""
        return f"{name}: {age}"

    result = introspect_function(sample_func)

    assert len(result["parameters"]) == 2
    assert result["parameters"][0]["type"] is object  # Any type
    assert result["parameters"][1]["type"] is object


def test_introspect_function_without_docstring():
    """Test introspection of a function without a docstring."""

    def sample_func(name: str, age: int):
        return f"{name}: {age}"

    result = introspect_function(sample_func)

    assert result["docstring"] == ""
