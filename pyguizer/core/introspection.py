"""Function Introspection Module"""

import inspect
from typing import Any, Dict, get_type_hints


def introspect_function(func: Any) -> Dict[str, Any]:
    """
    Introspect a function to extract signature, type hints, and docstring.

    Args:
        func: The function to introspect.

    Returns:
        A dictionary containing function metadata.
    """
    # Get function signature
    sig = inspect.signature(func)

    # Get type hints
    type_hints = get_type_hints(func)

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

    # Convert function name from snake_case to title case for display
    display_name = func.__name__.replace("_", " ").title()

    return {
        "name": func.__name__,  # Return original function name
        "display_name": display_name,  # Return display name separately
        "docstring": docstring,
        "parameters": parameters,
        "return_type": return_type,
    }
