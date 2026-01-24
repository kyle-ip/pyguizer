"""Widget Specification Object (WSO) Generation Module"""

import inspect
import enum
from typing import Any, Dict, List, Optional, Type, Union, get_args, get_origin
from pathlib import Path as PathType
from datetime import datetime as DateTimeType


class WidgetType:
    """Enum-like class for widget types."""
    TEXT = "text"
    NUMBER = "number"
    SLIDER = "slider"
    BOOLEAN = "boolean"
    MULTI_SELECT = "multi_select"
    SELECT = "select"
    JSON = "json"
    FILE_UPLOAD = "file_upload"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    COLOR = "color"


# Global widget registry for custom type mappings
WIDGET_REGISTRY = {
    "direct": {},  # Direct type mappings
    "inheritance": [],  # Inheritance-based mappings with priority
    "string": {}  # String-based mappings for dynamic types
}


def register_widget_mapping(py_type: Union[Type, str], widget_generator, priority: int = 0):
    """
    Register a custom widget mapping for a Python type.
    
    Args:
        py_type: Python type or string identifier to register.
        widget_generator: Function that returns (widget_type, constraints).
        priority: Priority for inheritance-based mappings (higher = more priority).
    """
    if isinstance(py_type, str):
        # Register as string-based mapping
        WIDGET_REGISTRY["string"][py_type] = widget_generator
    elif isinstance(py_type, type):
        # Register as both direct and inheritance mapping
        WIDGET_REGISTRY["direct"][py_type] = widget_generator
        # Add to inheritance registry with priority
        WIDGET_REGISTRY["inheritance"].append((priority, py_type, widget_generator))
        # Sort inheritance registry by priority (highest first)
        WIDGET_REGISTRY["inheritance"].sort(reverse=True, key=lambda x: x[0])
    else:
        raise TypeError(f"py_type must be a Type or str, got {type(py_type)}")


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
    
    # Check direct mapping first
    if py_type in WIDGET_REGISTRY["direct"]:
        return WIDGET_REGISTRY["direct"][py_type](py_type)
    
    # Check inheritance-based mappings
    for _, base_type, widget_generator in WIDGET_REGISTRY["inheritance"]:
        if inspect.isclass(py_type) and issubclass(py_type, base_type):
            return widget_generator(py_type)
    
    # Check string-based mapping for the type name
    type_name = getattr(py_type, "__name__", str(py_type))
    if type_name in WIDGET_REGISTRY["string"]:
        return WIDGET_REGISTRY["string"][type_name](py_type)
    
    # Check string-based mapping for the full module path
    full_type_name = f"{getattr(py_type, '__module__', '')}.{type_name}"
    if full_type_name in WIDGET_REGISTRY["string"]:
        return WIDGET_REGISTRY["string"][full_type_name](py_type)
    
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
    
    # Handle Decimal type
    try:
        from decimal import Decimal
        if py_type is Decimal:
            return WidgetType.NUMBER, {"decimal": True, "step": "0.01"}
    except ImportError:
        pass
    
    # Handle UUID type
    try:
        from uuid import UUID
        if py_type is UUID:
            return WidgetType.TEXT, {"pattern": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"}
    except ImportError:
        pass
    
    # Handle Path type for file upload
    if py_type is PathType or (origin and origin is PathType):
        return WidgetType.FILE_UPLOAD, {"accept": "*/*"}
    
    # Handle datetime types
    try:
        from datetime import date as DateType, time as TimeType
        if py_type is DateType:
            return WidgetType.DATE, {"format": "YYYY-MM-DD"}
        elif py_type is TimeType:
            return WidgetType.TIME, {"format": "HH:mm:ss"}
    except ImportError:
        pass
    
    if py_type is DateTimeType:
        return WidgetType.DATETIME, {"format": "YYYY-MM-DD HH:mm:ss"}
    
    # Handle Enum types
    if inspect.isclass(py_type) and issubclass(py_type, enum.Enum):
        options = [{
            "value": item.value,
            "label": item.name.replace("_", " ").title()
        } for item in py_type]
        return WidgetType.SELECT, {"options": options}
    
    # Handle List types
    if origin is list or origin is List:
        if args and args[0] is str:
            return WidgetType.MULTI_SELECT, {"options": []}
        return WidgetType.JSON, {}
    
    # Handle Set types
    if origin is set:
        if args and args[0] is str:
            return WidgetType.MULTI_SELECT, {"options": []}
        return WidgetType.JSON, {}
    
    # Handle Dict types
    if origin is dict:
        return WidgetType.JSON, {}
    
    # Handle Tuple types
    if origin is tuple:
        return WidgetType.JSON, {}
    
    # Handle FrozenSet types
    if origin is frozenset:
        if args and args[0] is str:
            return WidgetType.MULTI_SELECT, {"options": []}
        return WidgetType.JSON, {}
    
    # Handle Any type
    if py_type is Any:
        return WidgetType.TEXT, {}
    
    # Handle built-in and third-party classes by their attributes
    if inspect.isclass(py_type):
        # Check if it's a dataclass
        if hasattr(py_type, "__dataclass_fields__"):
            return WidgetType.JSON, {}
        
        # Check if it has a __str__ method that provides useful information
        if hasattr(py_type, "__str__") and py_type.__str__ is not object.__str__:
            return WidgetType.TEXT, {}
    
    # Default to text input
    return WidgetType.TEXT, {}
