"""Comprehensive unit tests for the introspection module."""

from typing import Any, Dict, List, Optional, Union

import pytest

from pyguizer.core.introspection import introspect_function


class TestIntrospectionBasic:
    """Test basic function introspection."""

    def test_simple_function(self):
        """Test introspection of a simple function."""

        def simple_func(x: int, y: str) -> bool:
            """Simple test function."""
            return True

        result = introspect_function(simple_func)

        assert result["name"] == "Simple Func"
        assert result["docstring"] == "Simple test function."
        assert result["return_type"] == bool
        assert len(result["parameters"]) == 2

        param_x = next(p for p in result["parameters"] if p["name"] == "x")
        assert param_x["type"] == int
        assert param_x["required"] is True
        assert param_x["default"] is None

        param_y = next(p for p in result["parameters"] if p["name"] == "y")
        assert param_y["type"] == str
        assert param_y["required"] is True

    def test_function_with_defaults(self):
        """Test introspection of function with default values."""

        def func_with_defaults(name: str, age: int = 25, active: bool = True) -> str:
            """Function with default parameters."""
            return f"{name}: {age}"

        result = introspect_function(func_with_defaults)

        assert len(result["parameters"]) == 3

        param_name = next(p for p in result["parameters"] if p["name"] == "name")
        assert param_name["required"] is True

        param_age = next(p for p in result["parameters"] if p["name"] == "age")
        assert param_age["required"] is False
        assert param_age["default"] == 25

        param_active = next(p for p in result["parameters"] if p["name"] == "active")
        assert param_active["required"] is False
        assert param_active["default"] is True

    def test_function_without_docstring(self):
        """Test introspection of function without docstring."""

        def no_docstring(x: int) -> int:
            return x * 2

        result = introspect_function(no_docstring)
        assert result["docstring"] == ""

    def test_function_with_complex_types(self):
        """Test introspection with complex type hints."""

        def complex_func(
            items: List[str], config: Dict[str, Any], value: Optional[int] = None
        ) -> Union[str, int]:
            """Function with complex types."""
            return "test"

        result = introspect_function(complex_func)

        assert len(result["parameters"]) == 3

        param_items = next(p for p in result["parameters"] if p["name"] == "items")
        assert "List" in str(param_items["type"])

        param_config = next(p for p in result["parameters"] if p["name"] == "config")
        assert "Dict" in str(param_config["type"])

        param_value = next(p for p in result["parameters"] if p["name"] == "value")
        assert param_value["required"] is False
        assert param_value["default"] is None

    def test_function_name_conversion(self):
        """Test that function names are converted to title case."""

        def snake_case_function_name() -> None:
            """Test function."""

        result = introspect_function(snake_case_function_name)
        assert result["name"] == "Snake Case Function Name"

    def test_function_with_no_parameters(self):
        """Test introspection of function with no parameters."""

        def no_params() -> str:
            """Function with no parameters."""
            return "test"

        result = introspect_function(no_params)
        assert len(result["parameters"]) == 0
        assert result["return_type"] == str

    def test_function_with_no_return_type_hint(self):
        """Test introspection of function without return type hint."""

        def no_return_hint(x: int):
            """Function without return type."""
            return x

        result = introspect_function(no_return_hint)
        assert result["return_type"] == Any

    def test_function_with_no_type_hints(self):
        """Test introspection of function without type hints."""

        def no_hints(x, y=10):
            """Function without type hints."""
            return x + y

        result = introspect_function(no_hints)
        assert len(result["parameters"]) == 2

        param_x = next(p for p in result["parameters"] if p["name"] == "x")
        assert param_x["type"] == Any
        assert param_x["required"] is True

        param_y = next(p for p in result["parameters"] if p["name"] == "y")
        assert param_y["required"] is False
        assert param_y["default"] == 10


class TestIntrospectionEdgeCases:
    """Test edge cases and error handling."""

    def test_nested_function(self):
        """Test introspection of nested function."""

        def outer():
            def inner(x: int) -> int:
                """Inner function."""
                return x

            return inner

        inner_func = outer()
        result = introspect_function(inner_func)
        assert result["name"] == "Inner"
        assert len(result["parameters"]) == 1

    def test_lambda_function(self):
        """Test introspection of lambda function."""
        lambda_func = lambda x: x * 2
        result = introspect_function(lambda_func)
        assert len(result["parameters"]) == 1

    def test_class_method(self):
        """Test introspection of class method."""

        class TestClass:
            def method(self, x: int) -> str:
                """Class method."""
                return str(x)

        result = introspect_function(TestClass.method)
        assert len(result["parameters"]) >= 1  # self is included

    def test_static_method(self):
        """Test introspection of static method."""

        class TestClass:
            @staticmethod
            def static_method(x: int) -> int:
                """Static method."""
                return x * 2

        result = introspect_function(TestClass.static_method)
        assert len(result["parameters"]) == 1


@pytest.mark.core
class TestIntrospectionParameterKinds:
    """Test different parameter kinds."""

    def test_positional_only(self):
        """Test positional-only parameters."""

        def pos_only(x: int, /) -> int:
            """Positional only."""
            return x

        result = introspect_function(pos_only)
        param = result["parameters"][0]
        assert param["kind"] == "POSITIONAL_ONLY"

    def test_keyword_only(self):
        """Test keyword-only parameters."""

        def kw_only(*, x: int) -> int:
            """Keyword only."""
            return x

        result = introspect_function(kw_only)
        param = result["parameters"][0]
        assert param["kind"] == "KEYWORD_ONLY"

    def test_var_positional(self):
        """Test *args parameter."""

        def var_pos(*args: int) -> int:
            """Variable positional."""
            return sum(args)

        result = introspect_function(var_pos)
        param = result["parameters"][0]
        assert param["kind"] == "VAR_POSITIONAL"

    def test_var_keyword(self):
        """Test **kwargs parameter."""

        def var_kw(**kwargs: Any) -> Dict:
            """Variable keyword."""
            return kwargs

        result = introspect_function(var_kw)
        param = result["parameters"][0]
        assert param["kind"] == "VAR_KEYWORD"
