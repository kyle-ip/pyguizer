"""Comprehensive unit tests for the widget module."""

import enum
from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple
from uuid import UUID


from pyguizer.core.widget import (
    WIDGET_REGISTRY,
    WidgetType,
    _map_type_to_widget,
    generate_wso,
    register_widget_mapping,
)


class TestWidgetBasicTypes:
    """Test widget generation for basic Python types."""

    def test_string_type(self):
        """Test string type mapping."""
        params = [
            {
                "name": "text",
                "type": str,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.TEXT
        assert wsos[0]["id"] == "text"
        assert wsos[0]["required"] is True

    def test_int_type(self):
        """Test integer type mapping."""
        params = [
            {
                "name": "count",
                "type": int,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.NUMBER
        assert "integer" in wsos[0]["constraints"]
        assert wsos[0]["constraints"]["integer"] is True

    def test_float_type(self):
        """Test float type mapping."""
        params = [
            {
                "name": "temperature",
                "type": float,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.SLIDER
        assert "min" in wsos[0]["constraints"]
        assert "max" in wsos[0]["constraints"]

    def test_bool_type(self):
        """Test boolean type mapping."""
        params = [
            {
                "name": "is_active",
                "type": bool,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.BOOLEAN

    def test_optional_type(self):
        """Test Optional type mapping."""
        params = [
            {
                "name": "value",
                "type": Optional[int],
                "default": None,
                "required": False,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.NUMBER
        assert wsos[0]["required"] is False


class TestWidgetComplexTypes:
    """Test widget generation for complex Python types."""

    def test_list_str_type(self):
        """Test List[str] type mapping."""
        params = [
            {
                "name": "items",
                "type": List[str],
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.MULTI_SELECT

    def test_list_other_type(self):
        """Test List[other] type mapping."""
        params = [
            {
                "name": "numbers",
                "type": List[int],
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.JSON

    def test_dict_type(self):
        """Test Dict type mapping."""
        params = [
            {
                "name": "config",
                "type": Dict[str, Any],
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.JSON

    def test_set_str_type(self):
        """Test Set[str] type mapping."""
        params = [
            {
                "name": "tags",
                "type": Set[str],
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.MULTI_SELECT

    def test_tuple_type(self):
        """Test Tuple type mapping."""
        params = [
            {
                "name": "coordinates",
                "type": Tuple[int, int],
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.JSON

    def test_frozenset_type(self):
        """Test FrozenSet type mapping."""
        params = [
            {
                "name": "immutable_set",
                "type": FrozenSet[str],
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.MULTI_SELECT


class TestWidgetSpecialTypes:
    """Test widget generation for special types."""

    def test_path_type(self):
        """Test Path type mapping."""
        params = [
            {
                "name": "file_path",
                "type": Path,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.FILE_UPLOAD
        assert "accept" in wsos[0]["constraints"]

    def test_date_type(self):
        """Test date type mapping."""
        params = [
            {
                "name": "birth_date",
                "type": date,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.DATE
        assert "format" in wsos[0]["constraints"]

    def test_time_type(self):
        """Test time type mapping."""
        params = [
            {
                "name": "meeting_time",
                "type": time,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.TIME

    def test_datetime_type(self):
        """Test datetime type mapping."""
        params = [
            {
                "name": "event_time",
                "type": datetime,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.DATETIME

    def test_decimal_type(self):
        """Test Decimal type mapping."""
        params = [
            {
                "name": "price",
                "type": Decimal,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.NUMBER
        assert "decimal" in wsos[0]["constraints"]

    def test_uuid_type(self):
        """Test UUID type mapping."""
        params = [
            {
                "name": "user_id",
                "type": UUID,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.TEXT
        assert "pattern" in wsos[0]["constraints"]

    def test_enum_type(self):
        """Test Enum type mapping."""

        class Color(enum.Enum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"

        params = [
            {
                "name": "color",
                "type": Color,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.SELECT
        assert "options" in wsos[0]["constraints"]
        assert len(wsos[0]["constraints"]["options"]) == 3


class TestWidgetWSOGeneration:
    """Test WSO generation functionality."""

    def test_multiple_parameters(self):
        """Test generating WSOs for multiple parameters."""
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
            {
                "name": "active",
                "type": bool,
                "default": True,
                "required": False,
                "kind": "POSITIONAL_OR_KEYWORD",
            },
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 3
        assert wsos[0]["id"] == "name"
        assert wsos[1]["id"] == "age"
        assert wsos[1]["default"] == 25
        assert wsos[2]["id"] == "active"
        assert wsos[2]["default"] is True

    def test_label_generation(self):
        """Test that labels are generated from parameter names."""
        params = [
            {
                "name": "user_name",
                "type": str,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert wsos[0]["label"] == "User Name"

    def test_data_type_preservation(self):
        """Test that data_type is preserved in WSO."""
        params = [
            {
                "name": "value",
                "type": List[str],
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert "List" in wsos[0]["data_type"]


class TestWidgetRegistry:
    """Test custom widget registry functionality."""

    def test_register_direct_mapping(self):
        """Test registering a direct type mapping."""

        def custom_widget_generator(py_type):
            return "custom_widget", {"custom": True}

        register_widget_mapping(str, custom_widget_generator)

        widget_type, constraints = _map_type_to_widget(str)
        assert widget_type == "custom_widget"
        assert constraints["custom"] is True

        # Clean up
        WIDGET_REGISTRY["direct"].pop(str, None)

    def test_register_string_mapping(self):
        """Test registering a string-based mapping."""

        def custom_widget_generator(py_type):
            return "string_widget", {}

        register_widget_mapping("CustomType", custom_widget_generator)

        # Clean up
        WIDGET_REGISTRY["string"].pop("CustomType", None)

    def test_register_inheritance_mapping(self):
        """Test registering an inheritance-based mapping."""

        class BaseType:
            pass

        class DerivedType(BaseType):
            pass

        def custom_widget_generator(py_type):
            return "inherited_widget", {}

        register_widget_mapping(BaseType, custom_widget_generator, priority=10)

        widget_type, constraints = _map_type_to_widget(DerivedType)
        assert widget_type == "inherited_widget"

        # Clean up
        WIDGET_REGISTRY["direct"].pop(BaseType, None)
        WIDGET_REGISTRY["inheritance"] = [
            item for item in WIDGET_REGISTRY["inheritance"] if item[1] != BaseType
        ]


class TestWidgetEdgeCases:
    """Test edge cases in widget generation."""

    def test_any_type(self):
        """Test Any type mapping."""
        params = [
            {
                "name": "dynamic",
                "type": Any,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.TEXT

    def test_dataclass_type(self):
        """Test dataclass type mapping."""
        from dataclasses import dataclass

        @dataclass
        class User:
            name: str
            age: int

        params = [
            {
                "name": "user",
                "type": User,
                "default": None,
                "required": True,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        ]
        wsos = generate_wso(params)

        assert len(wsos) == 1
        assert wsos[0]["type"] == WidgetType.JSON

    def test_empty_parameters(self):
        """Test generating WSOs with empty parameters."""
        wsos = generate_wso([])
        assert len(wsos) == 0
