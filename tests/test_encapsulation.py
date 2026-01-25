"""Test script to verify PyGUIzer encapsulation works correctly"""

from pyguizer import PyGUIzer

# Create a PyGUIzer instance with default layout
pyguizer = PyGUIzer()

# Define multiple functions with PyGUIzer decorator


@pyguizer
def greet(name: str, greeting: str = "Hello") -> str:
    """Generate a greeting message."""
    return f"{greeting}, {name}!"


@pyguizer
def calculate(a: int, b: int, operation: str = "add") -> int:
    """Perform a mathematical operation."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a // b
    else:
        raise ValueError(f"Unknown operation: {operation}")


@pyguizer
def format_text(text: str, uppercase: bool = False, reverse: bool = False) -> str:
    """Format text according to specified options."""
    result = text
    if uppercase:
        result = result.upper()
    if reverse:
        result = result[::-1]
    return result


if __name__ == "__main__":
    print("=== PyGUIzer Encapsulation Test ===")
    print("This script demonstrates that users don't need to write any FastAPI code.")
    print("Simply decorate functions with @PyGUIzer and call PyGUIzer.run()!")
    print("\nRegistered functions:")
    for func in PyGUIzer.registered_functions:
        print(f"  - {func.__name__}")
    print("\nTo run the server, uncomment the following line:")
    print("# PyGUIzer.run()")

    # Uncomment to actually run the server
    # PyGUIzer.run()
