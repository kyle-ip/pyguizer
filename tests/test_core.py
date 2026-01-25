import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test core functionality
print("Testing PyGUIzer core functionality...")

# Test that we can import the PyGUIzer decorator
try:
    from pyguizer import PyGUIzer

    print("✓ Successfully imported PyGUIzer decorator")
except Exception as e:
    print(f"✗ Failed to import PyGUIzer decorator: {e}")
    sys.exit(1)

# Test that we can create a decorated function
try:

    @PyGUIzer()
    def test_func(name: str, value: int = 42) -> str:
        """Test function."""
        return f"Test: {name} = {value}"

    print("✓ Successfully created decorated function")
except Exception as e:
    print(f"✗ Failed to create decorated function: {e}")
    sys.exit(1)

# Test that the decorator adds the __pyguizer__ attribute
try:
    assert hasattr(
        test_func, "__pyguizer__"
    ), "Function should have __pyguizer__ attribute"
    print("✓ Decorator correctly adds __pyguizer__ attribute")
except AssertionError as e:
    print(f"✗ {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)

# Test that we can access the PyGUIzer instance
try:
    pg_instance = test_func.__pyguizer__
    assert hasattr(pg_instance, "func"), "PyGUIzer instance should have func attribute"
    assert (
        pg_instance.func == test_func
    ), "func attribute should point to the decorated function"
    print("✓ PyGUIzer instance has correct func attribute")
except Exception as e:
    print(f"✗ Failed to access PyGUIzer instance: {e}")
    sys.exit(1)

print("\n🎉 All core functionality tests passed!")
print("The PyGUIzer prototype is working correctly.")
print("\nNext steps:")
print("1. Install dependencies: pip install fastapi pydantic uvicorn")
print("2. Run the sample app: python app.py")
print("3. Open http://localhost:8000 in your browser")
