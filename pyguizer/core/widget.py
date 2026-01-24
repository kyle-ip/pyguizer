"""Widget Specification Object (WSO) Generation Module"""

import inspect
from typing import Any, Dict, List, Optional, Type, Union, get_args, get_origin


class WidgetType:
    """Enum-like class for widget types."""
    TEXT = "text"
    NUMBER = "number"
    SLIDER = "slider"
    BOOLEAN = "boolean"
    MULTI_SELECT = "multi_select"
    SELECT = "select"
    JSON = "json"


def generate_wso(parameters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate Widget Specification Objects (WSOs) from function parameters.
    
    Args:
        parameters: List of parameter info dictionaries.
        
    Returns:
        List of Widget Specification Objects.
    """
    wsos = []
    
    for param in parameters:
        wso = {
            "id": param["name"],
            "label": param["name"].replace("_", " ").title(),
            "default": param["default"],
            "required": param["required"],
            "data_type": str(param["type"]),
            "constraints": {}
        }
        
        # Map Python type to widget type
        widget_type, constraints = _map_type_to_widget(param["type"])
        wso["type"] = widget_type
        wso["constraints"].update(constraints)
        
        wsos.append(wso)
    
    return wsos


def _map_type_to_widget(py_type: Type) -> tuple[str, Dict[str, Any]]:
    """
    Map Python type to widget type and constraints.
    
    Args:
        py_type: Python type to map.
        
    Returns:
        Tuple of (widget_type, constraints).
    """
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
    if origin is list or origin is List:
        if args and args[0] is str:
            return WidgetType.MULTI_SELECT, {"options": []}
        return WidgetType.JSON, {}
    
    # Handle Dict types
    if origin is dict or origin is Dict:
        return WidgetType.JSON, {}
    
    # Default to text input
    return WidgetType.TEXT, {}
