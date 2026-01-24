"""PyGUIzer - Automatic Web GUI Generator for Python Functions"""

__version__ = "0.1.0"

class PyGUIzer:
    """Decorator for generating web GUI from Python functions."""
    
    def __init__(self, layout=None):
        self.layout = layout or {"sections": [{"name": "Main", "widgets": []}]}
    
    def __call__(self, func):
        self.func = func
        # Store a reference to this PyGUIzer instance on the function
        func.__pyguizer__ = self
        return func

# Lazy import core components to avoid circular dependencies and heavy imports

def __getattr__(name):
    """Lazy import for core components."""
    if name == "introspect_function":
        from pyguizer.core.introspection import introspect_function
        return introspect_function
    elif name == "generate_wso":
        from pyguizer.core.widget import generate_wso
        return generate_wso
    elif name == "create_app":
        from pyguizer.api.app import create_app
        return create_app
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# Export main components
export = {
    "PyGUIzer": PyGUIzer,
}

