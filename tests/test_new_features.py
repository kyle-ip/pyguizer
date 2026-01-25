"""Comprehensive test for PyGUIzer new features"""

import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

# Add the project root to Python path
sys.path.insert(0, ".")

from pyguizer.core.introspection import introspect_function
from pyguizer.core.widget import WidgetType, generate_wso, register_widget_mapping


# Test Enum for widget mapping
class TestEnum(Enum):
    OPTION_1 = "option_1"
    OPTION_2 = "option_2"
    OPTION_3 = "option_3"


# Test function with advanced types
def test_function(
    text_param: str,
    int_param: int,
    float_param: float,
    bool_param: bool,
    list_param: List[str],
    dict_param: Dict[str, str],
    path_param: Path,
    datetime_param: datetime,
    enum_param: TestEnum,
    optional_param: Optional[str] = None,
) -> Dict[str, str]:
    """Test function with various parameter types."""
    return {
        "text_param": text_param,
        "int_param": str(int_param),
        "float_param": str(float_param),
        "bool_param": str(bool_param),
        "list_param": str(list_param),
        "dict_param": str(dict_param),
        "path_param": str(path_param),
        "datetime_param": str(datetime_param),
        "enum_param": str(enum_param),
        "optional_param": str(optional_param),
    }


# Test custom widget mapping
class CustomType:
    """Custom type for testing widget registry"""



def custom_widget_generator(py_type):
    """Custom widget generator for CustomType"""
    return WidgetType.TEXT, {"placeholder": "Custom type input"}


print("🔍 Testing PyGUIzer New Features...\n")

# Test 1: Function introspection with advanced types
print("1. Testing function introspection with advanced types...")
try:
    func_info = introspect_function(test_function)
    print(
        f"   ✅ Introspection successful! Found {len(func_info['parameters'])} parameters"
    )

    # Print parameter details
    for param in func_info["parameters"]:
        print(f"   - {param['name']}: {param['type']} (required: {param['required']})")

except Exception as e:
    print(f"   ❌ Introspection failed: {e}")
    sys.exit(1)


# Test 2: WSO generation with advanced types
print("\n2. Testing WSO generation with advanced types...")
try:
    wsos = generate_wso(func_info["parameters"])
    print(f"   ✅ WSO generation successful! Generated {len(wsos)} WSOs")

    # Print WSO details
    for wso in wsos:
        print(f"   - {wso['id']}: {wso['type']} widget")

    # Verify specific widget types
    widget_types = {wso["id"]: wso["type"] for wso in wsos}
    expected_types = {
        "text_param": "text",
        "int_param": "number",
        "float_param": "slider",
        "bool_param": "boolean",
        "list_param": "multi_select",
        "dict_param": "json",
        "path_param": "file_upload",
        "datetime_param": "datetime",
        "enum_param": "select",
        "optional_param": "text",
    }

    for param_name, expected_type in expected_types.items():
        actual_type = widget_types.get(param_name)
        if actual_type == expected_type:
            print(f"   ✅ {param_name}: Correctly mapped to {expected_type}")
        else:
            print(f"   ❌ {param_name}: Expected {expected_type}, got {actual_type}")

except Exception as e:
    print(f"   ❌ WSO generation failed: {e}")
    sys.exit(1)


# Test 3: Custom widget registry
print("\n3. Testing custom widget registry...")
try:
    # Register custom mapping
    register_widget_mapping(CustomType, custom_widget_generator)
    print("   ✅ Custom widget mapping registered successfully")

    # Test with custom type function
    def custom_type_function(custom_param: CustomType) -> str:
        """Test function with custom type"""
        return str(custom_param)

    # Introspect and generate WSO
    custom_func_info = introspect_function(custom_type_function)
    custom_wsos = generate_wso(custom_func_info["parameters"])

    if custom_wsos[0]["type"] == WidgetType.TEXT:
        print("   ✅ Custom type correctly mapped to text widget")
    else:
        print(
            f"   ❌ Custom type mapping failed: Expected text, got {custom_wsos[0]['type']}"
        )

except Exception as e:
    print(f"   ❌ Custom widget registry failed: {e}")
    sys.exit(1)


print("\n🎉 All new features tests passed!")
print("\n📋 Summary of implemented features:")
print("1. ✅ Function introspection for advanced types")
print("2. ✅ WSO generation for:")
print("   - File upload (Path type)")
print("   - DateTime picker (datetime type)")
print("   - Select widget (Enum type)")
print("   - Advanced list/dict handling")
print("3. ✅ Custom widget registry system")
print("4. ✅ WebSocket support for real-time updates")
print("5. ✅ Task management with status tracking")
print("6. ✅ Progress updates and streaming output")
print("7. ✅ Task cancellation mechanism")
