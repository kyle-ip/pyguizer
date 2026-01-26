"""
Simple PyGUIzer Example for Deployment Demonstration

This example shows how to create a basic PyGUIzer application
that can be easily packaged into a standalone executable.
"""

from typing import List, Optional
from pyguizer import PyGUIzer

# Create a PyGUIzer instance
pyguizer = PyGUIzer()


@pyguizer
def greet(name: str, age: int, hobbies: List[str] = None, is_active: bool = True) -> str:
    """Generate a personalized greeting message."""
    hobbies_str = f" and enjoy {', '.join(hobbies)}" if hobbies else ""
    status_str = "active" if is_active else "inactive"
    return f"Hello {name}! You are {age} years old, {status_str}{hobbies_str}."


@pyguizer
def calculate_discount(price: float, discount_percentage: float, is_vip: bool = False) -> float:
    """Calculate the final price after applying discounts."""
    base_discount = price * (discount_percentage / 100)
    vip_bonus = price * 0.05 if is_vip else 0
    total_discount = base_discount + vip_bonus
    final_price = price - total_discount
    return round(final_price, 2)


@pyguizer
def convert_temperature(celsius: float, to_unit: str = "fahrenheit") -> float:
    """Convert temperature between Celsius and Fahrenheit."""
    if to_unit.lower() == "fahrenheit":
        return (celsius * 9/5) + 32
    elif to_unit.lower() == "celsius":
        return celsius
    else:
        raise ValueError("Invalid unit. Use 'fahrenheit' or 'celsius'.")


if __name__ == "__main__":
    print("=== PyGUIzer Simple Example ===")
    print("This example demonstrates how to create a PyGUIzer application")
    print("that can be easily packaged into a standalone executable.")
    print("\nAvailable functions:")
    for func in pyguizer.registered_functions:
        print(f"  - {func.__name__}: {func.__doc__.splitlines()[0]}")
    print("\nTo run the app directly:")
    print("  python examples/simple_deploy_example.py")
    print("\nTo package into a standalone executable:")
    print("  python -m pyguizer package examples/simple_deploy_example.py")
    print("\nTo run with PyGUIzer CLI:")
    print("  python -m pyguizer run examples/simple_deploy_example.py")
    
    # Run the server
    pyguizer.run(title="Simple PyGUIzer Example", port=8000)
