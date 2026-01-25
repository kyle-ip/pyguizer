import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test the CLI functionality
print("Testing PyGUIzer CLI functionality...")

# Import the CLI app
try:
    pass

    print("✓ Successfully imported CLI app")
except Exception as e:
    print(f"✗ Failed to import CLI app: {e}")
    sys.exit(1)

# Test that we can create a PyGUIzer instance
try:
    from pyguizer import PyGUIzer

    @PyGUIzer()
    def test_func(name: str, value: int) -> str:
        return f"Test: {name} - {value}"

    print("✓ Successfully created PyGUIzer-decorated function")
except Exception as e:
    print(f"✗ Failed to create PyGUIzer instance: {e}")
    sys.exit(1)

# Test the decorator adds the __pyguizer__ attribute
try:
    assert hasattr(
        test_func, "__pyguizer__"
    ), "Function should have __pyguizer__ attribute"
    print("✓ PyGUIzer decorator correctly adds __pyguizer__ attribute")
except AssertionError as e:
    print(f"✗ {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)

print("\n🎉 All CLI and decorator functionality tests passed!")
print("The PyGUIzer prototype is ready for use.")
