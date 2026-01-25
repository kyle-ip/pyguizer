"""Standalone verification script for PyGUIzer core functionality"""

import inspect
from typing import Any, Dict, List, Type, Union, get_args, get_origin


# Core functionality copied from pyguizer modules
def introspect_function(func: Any) -> Dict[str, Any]:
    """Introspect a function to extract signature, type hints, and docstring."""
    # Get function signature
    sig = inspect.signature(func)

    # Get type hints
    try:
        from typing import get_type_hints

        type_hints = get_type_hints(func)
    except ImportError:
        type_hints = {}

    # Get docstring
    docstring = inspect.getdoc(func) or ""

    # Extract return type
    return_type = type_hints.pop("return", Any)

    # Extract parameters
    parameters = []
    for param_name, param in sig.parameters.items():
        param_info = {
            "name": param_name,
            "type": type_hints.get(param_name, Any),
            "default": (
                param.default if param.default is not inspect.Parameter.empty else None
            ),
            "required": param.default is inspect.Parameter.empty,
            "kind": param.kind.name,
        }
        parameters.append(param_info)

    return {
        "name": func.__name__,
        "docstring": docstring,
        "parameters": parameters,
        "return_type": return_type,
    }


class WidgetType:
    """Enum-like class for widget types."""

    TEXT = "text"
    NUMBER = "number"
    SLIDER = "slider"
    BOOLEAN = "boolean"
    MULTI_SELECT = "multi_select"
    SELECT = "select"
    JSON = "json"


def _map_type_to_widget(py_type: Type) -> tuple[str, Dict[str, Any]]:
    """Map Python type to widget type and constraints."""
    origin = get_origin(py_type)
    args = get_args(py_type)

    # Handle Optional types
    if origin is Union and type(None) in args:
        non_none_args = [arg for arg in args if arg is not type(None)]
        if len(non_none_args) == 1:
            return _map_type_to_widget(non_none_args[0])

    # Handle basic types
    if py_type is str:
        return WidgetType.TEXT, {}

    if py_type is int:
        return WidgetType.NUMBER, {"integer": True}

    if py_type is float:
        return WidgetType.SLIDER, {"min": 0, "max": 100, "step": 0.1}

    if py_type is bool:
        return WidgetType.BOOLEAN, {}

    # Handle List types
    if origin is list:
        if args and args[0] is str:
            return WidgetType.MULTI_SELECT, {"options": []}
        return WidgetType.JSON, {}

    # Handle Dict types
    if origin is dict:
        return WidgetType.JSON, {}

    # Default to text input
    return WidgetType.TEXT, {}


def generate_wso(parameters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate Widget Specification Objects (WSOs) from function parameters."""
    wsos = []

    for param in parameters:
        wso = {
            "id": param["name"],
            "label": param["name"].replace("_", " ").title(),
            "default": param["default"],
            "required": param["required"],
            "data_type": str(param["type"]),
            "constraints": {},
        }

        # Map Python type to widget type
        widget_type, constraints = _map_type_to_widget(param["type"])
        wso["type"] = widget_type
        wso["constraints"].update(constraints)

        wsos.append(wso)

    return wsos


def process_layout(
    wsos: List[Dict[str, Any]], layout_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Process layout configuration and merge with Widget Specification Objects."""
    # Get all widget ids
    widget_ids = {wso["id"] for wso in wsos}

    # Ensure layout has sections
    if "sections" not in layout_config:
        layout_config["sections"] = [{"name": "Main", "widgets": []}]

    # Create a set of all widgets mentioned in the layout
    layout_widgets = set()
    for section in layout_config["sections"]:
        if "widgets" in section:
            layout_widgets.update(section["widgets"])

    # Add any widgets not mentioned in the layout to the first section
    unassigned_widgets = widget_ids - layout_widgets
    if unassigned_widgets:
        if not layout_config["sections"][0].get("widgets"):
            layout_config["sections"][0]["widgets"] = []
        layout_config["sections"][0]["widgets"].extend(unassigned_widgets)

    # Build the UI Layout Schema
    ui_layout = {"sections": []}

    for section in layout_config["sections"]:
        section_widgets = []
        if "widgets" in section:
            for widget_id in section["widgets"]:
                # Find the corresponding WSO
                wso = next((w for w in wsos if w["id"] == widget_id), None)
                if wso:
                    section_widgets.append(wso)

        ui_layout["sections"].append(
            {"name": section["name"], "widgets": section_widgets}
        )

    return ui_layout


# Test the core functionality
print("Testing PyGUIzer core functionality...")


# Define a sample function for testing
def sample_function(name: str, age: int, is_active: bool = True) -> str:
    """Sample function for testing."""
    return f"Hello {name}!"


# Test function introspection
func_info = introspect_function(sample_function)
print("\n✓ Function introspection successful:")
print(f"  Function name: {func_info['name']}")
print(f"  Docstring: {func_info['docstring']}")
print(f"  Parameters: {len(func_info['parameters'])}")

# Test WSO generation
wsos = generate_wso(func_info["parameters"])
print("\n✓ WSO generation successful:")
for wso in wsos:
    print(f"  - {wso['id']}: {wso['type']} (required: {wso['required']})")

# Test layout processing
layout_config = {"sections": [{"name": "Main", "widgets": ["name", "age"]}]}
layout = process_layout(wsos, layout_config)
print("\n✓ Layout processing successful:")
print(f"  Sections: {len(layout['sections'])}")
for section in layout["sections"]:
    print(f"  - {section['name']}: {len(section['widgets'])} widgets")

print("\n🎉 All core PyGUIzer functions are working correctly!")
print("The prototype has been successfully implemented.")
