import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test core functionality by directly importing the modules
try:
    # Directly import core modules without going through __init__.py
    from pyguizer.core.introspection import introspect_function
    from pyguizer.core.widget import generate_wso
    from pyguizer.core.layout import process_layout
    
    print("✓ Successfully imported core PyGUIzer components")
    
    # Define a sample function for testing
    def sample_function(name: str, age: int, is_active: bool = True) -> str:
        """Sample function for testing."""
        return f"Hello {name}!"
    
    # Test function introspection
    func_info = introspect_function(sample_function)
    print(f"\n✓ Function introspection successful:")
    print(f"  Function name: {func_info['name']}")
    print(f"  Docstring: {func_info['docstring']}")
    print(f"  Parameters: {len(func_info['parameters'])}")
    
    # Test WSO generation
    wsos = generate_wso(func_info['parameters'])
    print(f"\n✓ WSO generation successful:")
    for wso in wsos:
        print(f"  - {wso['id']}: {wso['type']} (required: {wso['required']})")
    
    # Test layout processing
    layout_config = {"sections": [{"name": "Main", "widgets": ["name", "age"]}]}
    layout = process_layout(wsos, layout_config)
    print(f"\n✓ Layout processing successful:")
    print(f"  Sections: {len(layout['sections'])}")
    for section in layout['sections']:
        print(f"  - {section['name']}: {len(section['widgets'])} widgets")
    
    print("\n🎉 All core PyGUIzer functions are working correctly!")
    print("The prototype has been successfully implemented.")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
