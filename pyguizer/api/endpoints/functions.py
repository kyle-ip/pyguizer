"""Function-related endpoints for PyGUIzer"""

from fastapi import APIRouter, Depends, HTTPException

from pyguizer.api.dependencies import get_pyguizer_app

router = APIRouter(prefix="/api/functions", tags=["functions"])


@router.get(
    "",
    summary="Get All Functions",
    description="Retrieve a list of all registered functions with their "
    "basic information",
)
async def get_functions(pyguizer_app=Depends(get_pyguizer_app)):
    """Get all registered functions.

    Returns:
        List of functions with their name, display name, and description
    """
    return [
        {
            "name": func_name,
            "display_name": func_data["func_info"]["name"],
            "description": func_data["func_info"]["docstring"],
        }
        for func_name, func_data in pyguizer_app.function_registry.items()
    ]


@router.get(
    "/{func_name}",
    summary="Get Function Details",
    description="Retrieve detailed information about a specific function",
    openapi_extra={
        "examples": {
            "GetAddFunction": {
                "summary": "Get Add Function Details",
                "description": "Retrieve details for the add function",
                "value": {"func_name": "add"},
            },
            "GetMultiplyFunction": {
                "summary": "Get Multiply Function Details",
                "description": "Retrieve details for the multiply function",
                "value": {"func_name": "multiply"},
            },
            "GetAsyncAddFunction": {
                "summary": "Get Async Add Function Details",
                "description": "Retrieve details for the async_add function",
                "value": {"func_name": "async_add"},
            },
        }
    },
)
async def get_function(func_name: str, pyguizer_app=Depends(get_pyguizer_app)):
    """Get details for a specific function.

    Args:
        func_name: The name of the function to retrieve details for

    Returns:
        Detailed information about the function, including parameters,
        outputs, and layout
    """
    # Check if function exists first (before any processing)
    if func_name not in pyguizer_app.function_registry:
        raise HTTPException(status_code=404, detail=f"Function '{func_name}' not found")

    try:
        func_data = pyguizer_app.function_registry[func_name]

        # Convert parameter types to strings for JSON serialization
        parameters = []
        for param in func_data["func_info"]["parameters"]:
            param_copy = param.copy()
            param_type = param_copy["type"]
            # Handle different type representations
            if hasattr(param_type, "__name__"):
                param_copy["type"] = param_type.__name__
            elif hasattr(param_type, "_name"):
                param_copy["type"] = param_type._name
            else:
                param_copy["type"] = str(param_type)
            parameters.append(param_copy)

        # Check if layout is serializable
        layout = func_data["ui_layout"]

        # Determine output information
        return_type = func_data["func_info"]["return_type"]
        outputs = []

        # If return type is a dict or tuple, we can extract multiple outputs
        # For now, we'll always include "result" as the default output
        # and add additional outputs if the return type suggests multiple values
        outputs.append(
            {
                "name": "result",
                "type": (
                    str(return_type)
                    if hasattr(return_type, "__name__")
                    else str(return_type)
                ),
                "description": "Function return value",
            }
        )

        # Check if return type is a tuple or dict to suggest multiple outputs
        if hasattr(return_type, "__origin__"):
            origin = return_type.__origin__
            if origin is dict:
                # For dict returns, we could extract keys, but that
                # requires runtime info
                # For now, just use "result"
                pass
            elif origin is tuple:
                # For tuple returns, we could suggest indexed outputs
                # But we'll keep it simple and just use "result" for now
                pass

        return {
            "name": func_name,
            "display_name": func_data["func_info"]["name"],
            "description": func_data["func_info"]["docstring"],
            "parameters": parameters,
            "outputs": outputs,
            "layout": layout,
        }
    except Exception as e:
        # Log the detailed error for debugging
        import traceback

        print(f"Error in get_function for {func_name}: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
