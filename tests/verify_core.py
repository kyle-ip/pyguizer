import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Verifying PyGUIzer Core Functionality...\n")

# Test 1: Import PyGUIzer decorator
try:
    from pyguizer import PyGUIzer

    print("✅ Test 1 passed: PyGUIzer decorator imported successfully")
except Exception as e:
    print(f"❌ Test 1 failed: {e}")
    sys.exit(1)

# Test 2: Create a decorated function
try:
    from typing import List

    @PyGUIzer()
    def test_function(
        name: str, age: int, hobbies: List[str] = None, active: bool = True
    ) -> str:
        """Test function with various types."""
        hobbies_str = f" and enjoy {', '.join(hobbies)}" if hobbies else ""
        status = "active" if active else "inactive"
        return f"Hello {name}! You are {age} years old, {status}{hobbies_str}."

    print("✅ Test 2 passed: Decorated function created successfully")
except Exception as e:
    print(f"❌ Test 2 failed: {e}")
    sys.exit(1)

# Test 3: Check if __pyguizer__ attribute is added
try:
    assert hasattr(test_function, "__pyguizer__"), "Missing __pyguizer__ attribute"
    print("✅ Test 3 passed: __pyguizer__ attribute added correctly")
except AssertionError as e:
    print(f"❌ Test 3 failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test 3 failed: {e}")
    sys.exit(1)

# Test 4: Check PyGUIzer instance attributes
try:
    pg_instance = test_function.__pyguizer__
    assert hasattr(pg_instance, "func"), "Missing func attribute"
    assert (
        pg_instance.func == test_function
    ), "func attribute doesn't point to the decorated function"
    assert hasattr(pg_instance, "layout"), "Missing layout attribute"
    print("✅ Test 4 passed: PyGUIzer instance has correct attributes")
except AssertionError as e:
    print(f"❌ Test 4 failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test 4 failed: {e}")
    sys.exit(1)

# Test 5: Import core modules directly
try:
    from pyguizer.core.introspection import introspect_function
    from pyguizer.core.layout import process_layout
    from pyguizer.core.widget import generate_wso

    print("✅ Test 5 passed: Core modules imported successfully")
except Exception as e:
    print(f"❌ Test 5 failed: {e}")
    sys.exit(1)

# Test 6: Test type introspection
try:
    func_info = introspect_function(test_function)
    assert func_info["name"] == "test_function"
    assert len(func_info["parameters"]) == 4
    print("✅ Test 6 passed: Function introspection works correctly")
except Exception as e:
    print(f"❌ Test 6 failed: {e}")
    sys.exit(1)

# Test 7: Test WSO generation
try:
    wsos = generate_wso(func_info["parameters"])
    assert len(wsos) == 4
    print("✅ Test 7 passed: WSO generation works correctly")
except Exception as e:
    print(f"❌ Test 7 failed: {e}")
    sys.exit(1)

# Test 8: Test layout processing
try:
    layout_config = {"sections": [{"name": "Main", "widgets": ["name", "age"]}]}
    layout = process_layout(wsos, layout_config)
    assert (
        len(layout["sections"]) == 1
    ), f"Expected 1 section, got {len(layout['sections'])}"
    # Should have at least 2 widgets, plus any unassigned ones
    widget_count = len(layout["sections"][0]["widgets"])
    assert widget_count >= 2, f"Expected at least 2 widgets, got {widget_count}"
    print("✅ Test 8 passed: Layout processing works correctly")
    print(f"    (found {len(layout['sections'][0]['widgets'])} widgets)")
except AssertionError as e:
    print(f"❌ Test 8 failed: Assertion error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test 8 failed: Exception: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n🎉 All core functionality tests passed!")
print("\n📋 Summary:")
print("- PyGUIzer decorator works correctly")
print("- Function introspection is functional")
print("- WSO generation works for standard types")
print("- Layout processing is operational")
print("🚀 Next steps:")
print("1. Install dependencies in the correct Python environment")
print("2. Try running the CLI command:")
print("   python -m pyguizer run app.py")
print("3. Check that the Python path is correctly set")
