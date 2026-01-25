"""Regression tests to ensure core functionality continues to work."""

import pytest
from fastapi.testclient import TestClient

from pyguizer import PyGUIzer
from pyguizer.api.app import PyGUIzerApp, create_app
from pyguizer.core.introspection import introspect_function
from pyguizer.core.layout import process_layout
from pyguizer.core.widget import generate_wso


class TestRegressionCore:
    """Regression tests for core functionality."""

    def test_decorator_regression(self):
        """Ensure PyGUIzer decorator still works correctly."""
        pyguizer = PyGUIzer()

        @pyguizer
        def test_func(name: str, age: int = 25) -> str:
            """Test function."""
            return f"{name}: {age}"

        assert hasattr(test_func, "__pyguizer__")
        assert test_func in PyGUIzer.registered_functions

    def test_introspection_regression(self):
        """Ensure function introspection still works."""

        def sample_func(x: int, y: str) -> bool:
            """Sample function."""
            return True

        result = introspect_function(sample_func)

        assert result["name"] == "sample_func"
        assert result["display_name"] == "Sample Func"
        assert len(result["parameters"]) == 2
        assert result["return_type"] == bool

    def test_wso_generation_regression(self):
        """Ensure WSO generation still works."""
        params = [
            {
                "name": "name",
                "type": str,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            },
            {
                "name": "age",
                "type": int,
                "default": 25,
                "required": False,
                "kind": "POSITIONAL_OR_KEYWORD",
            },
        ]

        wsos = generate_wso(params)

        assert len(wsos) == 2
        assert wsos[0]["id"] == "name"
        assert wsos[1]["id"] == "age"
        assert wsos[1]["default"] == 25

    def test_layout_processing_regression(self):
        """Ensure layout processing still works."""
        wsos = [
            {"id": "name", "label": "Name", "type": "text", "required": True},
            {"id": "age", "label": "Age", "type": "number", "required": True},
        ]
        layout_config = {"sections": [{"name": "Main", "widgets": ["name", "age"]}]}

        result = process_layout(wsos, layout_config)

        assert "containers" in result
        assert len(result["containers"]) == 1
        assert len(result["containers"][0]["widgets"]) == 2


class TestRegressionAPI:
    """Regression tests for API endpoints."""

    @pytest.fixture
    def test_app(self):
        """Create a test app with sample functions."""

        def add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b

        app = PyGUIzerApp()
        app.register_function(add)
        return create_app(pyguizer_app=app)

    def test_spec_endpoint_regression(self, test_app):
        """Ensure /api/spec endpoint still works."""
        client = TestClient(test_app)
        response = client.get("/api/spec")

        assert response.status_code == 200
        spec = response.json()
        assert "name" in spec
        assert "functions" in spec

    def test_run_endpoint_regression(self, test_app):
        """Ensure /api/run endpoint still works."""
        client = TestClient(test_app)
        response = client.post(
            "/api/run", json={"func_name": "add", "inputs": {"a": 5, "b": 3}}
        )

        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert "status" in data

    def test_functions_endpoint_regression(self, test_app):
        """Ensure /api/functions endpoint still works."""
        client = TestClient(test_app)
        response = client.get("/api/functions")

        assert response.status_code == 200
        functions = response.json()
        assert isinstance(functions, list)
        assert len(functions) > 0


class TestRegressionMultiFunction:
    """Regression tests for multi-function support."""

    @pytest.fixture
    def multi_function_app(self):
        """Create app with multiple functions."""

        def add(a: int, b: int) -> int:
            return a + b

        def multiply(x: float, y: float) -> float:
            return x * y

        app = PyGUIzerApp()
        app.register_function(add)
        app.register_function(multiply)
        return create_app(pyguizer_app=app)

    def test_multi_function_spec_regression(self, multi_function_app):
        """Ensure multi-function spec still works."""
        client = TestClient(multi_function_app)
        response = client.get("/api/spec")

        spec = response.json()
        assert len(spec["functions"]) == 2

    def test_multi_function_execution_regression(self, multi_function_app):
        """Ensure running different functions still works."""
        client = TestClient(multi_function_app)

        # Run first function
        response1 = client.post(
            "/api/run", json={"func_name": "add", "inputs": {"a": 5, "b": 3}}
        )
        assert response1.status_code == 200

        # Run second function
        response2 = client.post(
            "/api/run", json={"func_name": "multiply", "inputs": {"x": 2.5, "y": 4.0}}
        )
        assert response2.status_code == 200


class TestRegressionTypeMapping:
    """Regression tests for type-to-widget mapping."""

    def test_basic_types_regression(self):
        """Ensure basic type mappings still work."""
        from typing import Dict, List, Optional

        test_cases = [
            (str, "text"),
            (int, "number"),
            (float, "slider"),
            (bool, "boolean"),
            (List[str], "multi_select"),
            (Dict, "json"),
            (Optional[int], "number"),
        ]

        for py_type, expected_widget in test_cases:
            params = [
                {
                    "name": "test",
                    "type": py_type,
                    "default": None,
                    "required": True,
                    "kind": "POSITIONAL_OR_KEYWORD",
                }
            ]
            wsos = generate_wso(params)
            assert wsos[0]["type"] == expected_widget, f"Failed for {py_type}"

    def test_special_types_regression(self):
        """Ensure special type mappings still work."""
        import enum
        from datetime import date, datetime, time
        from decimal import Decimal
        from pathlib import Path
        from uuid import UUID

        class TestEnum(enum.Enum):
            VALUE1 = "value1"
            VALUE2 = "value2"

        test_cases = [
            (Path, "file_upload"),
            (date, "date"),
            (time, "time"),
            (datetime, "datetime"),
            (Decimal, "number"),
            (UUID, "text"),
            (TestEnum, "select"),
        ]

        for py_type, expected_widget in test_cases:
            params = [
                {
                    "name": "test",
                    "type": py_type,
                    "default": None,
                    "required": True,
                    "kind": "POSITIONAL_OR_KEYWORD",
                }
            ]
            wsos = generate_wso(params)
            assert wsos[0]["type"] == expected_widget, f"Failed for {py_type}"


class TestRegressionBackwardCompatibility:
    """Regression tests for backward compatibility."""

    def test_sections_key_compatibility(self):
        """Ensure sections key still works for backward compatibility."""
        wsos = [{"id": "name", "label": "Name", "type": "text", "required": True}]
        layout_config = {"sections": [{"name": "Main", "widgets": ["name"]}]}

        result = process_layout(wsos, layout_config)

        # Should have containers
        assert "containers" in result
        # Should also have sections for backward compatibility
        assert "sections" in result or len(result["containers"]) > 0

    def test_old_api_format_compatibility(self):
        """Ensure old API response format still works."""

        def test_func(x: int) -> int:
            return x

        app = PyGUIzerApp()
        app.register_function(test_func)
        fastapi_app = create_app(pyguizer_app=app)
        client = TestClient(fastapi_app)

        response = client.get("/api/spec")
        spec = response.json()

        # Should have required fields
        assert "name" in spec
        assert "functions" in spec
        assert isinstance(spec["functions"], list)
