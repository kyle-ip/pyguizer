#!/usr/bin/env python3
"""
Test script to verify layout enhancements for Phase 3 development.
This script tests the new layout processing functionality without requiring all dependencies.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath("."))

from pyguizer.core.layout import process_layout

def test_basic_section_layout():
    """Test basic section layout (backward compatibility)"""
    print("=== Testing Basic Section Layout ===")
    
    wsos = [
        {"id": "param1", "type": "text", "label": "Param 1"},
        {"id": "param2", "type": "number", "label": "Param 2"}
    ]
    
    layout_config = {
        "sections": [
            {"name": "Main", "widgets": ["param1"]}
        ]
    }
    
    result = process_layout(wsos, layout_config)
    print(f"Result: {result}")
    
    # Verify backward compatibility - sections key should still exist
    assert "sections" in result
    assert len(result["sections"]) == 1
    assert result["sections"][0]["name"] == "Main"
    assert len(result["sections"][0]["widgets"]) == 2  # Includes unassigned param2
    assert "containers" in result
    
    print("✓ Basic section layout test passed!")
    print()

def test_tabs_layout():
    """Test tabs layout"""
    print("=== Testing Tabs Layout ===")
    
    wsos = [
        {"id": "param1", "type": "text", "label": "Param 1"},
        {"id": "param2", "type": "number", "label": "Param 2"},
        {"id": "param3", "type": "boolean", "label": "Param 3"}
    ]
    
    layout_config = {
        "containers": [
            {
                "type": "tabs",
                "tabs": [
                    {"name": "Tab 1", "widgets": ["param1"]},
                    {"name": "Tab 2", "widgets": ["param2"]}
                ]
            }
        ]
    }
    
    result = process_layout(wsos, layout_config)
    print(f"Result: {result}")
    
    # Verify tabs structure
    assert "containers" in result
    assert len(result["containers"]) == 1
    assert result["containers"][0]["type"] == "tabs"
    assert len(result["containers"][0]["tabs"]) == 2
    assert result["containers"][0]["tabs"][0]["name"] == "Tab 1"
    assert result["containers"][0]["tabs"][1]["name"] == "Tab 2"
    
    # Verify all widgets are included (param3 should be in first tab due to being unassigned)
    assert len(result["containers"][0]["tabs"][0]["widgets"]) == 2  # param1 + param3
    
    print("✓ Tabs layout test passed!")
    print()

def test_accordion_layout():
    """Test accordion layout"""
    print("=== Testing Accordion Layout ===")
    
    wsos = [
        {"id": "param1", "type": "text", "label": "Param 1"},
        {"id": "param2", "type": "number", "label": "Param 2"}
    ]
    
    layout_config = {
        "containers": [
            {
                "type": "accordion",
                "items": [
                    {"name": "Section 1", "widgets": ["param1"]},
                    {"name": "Section 2", "widgets": ["param2"]}
                ]
            }
        ]
    }
    
    result = process_layout(wsos, layout_config)
    print(f"Result: {result}")
    
    # Verify accordion structure
    assert "containers" in result
    assert len(result["containers"]) == 1
    assert result["containers"][0]["type"] == "accordion"
    assert len(result["containers"][0]["items"]) == 2
    
    print("✓ Accordion layout test passed!")
    print()

def test_grid_layout():
    """Test grid layout"""
    print("=== Testing Grid Layout ===")
    
    wsos = [
        {"id": "param1", "type": "text", "label": "Param 1"},
        {"id": "param2", "type": "number", "label": "Param 2"},
        {"id": "param3", "type": "boolean", "label": "Param 3"},
        {"id": "param4", "type": "slider", "label": "Param 4"}
    ]
    
    layout_config = {
        "containers": [
            {
                "type": "grid",
                "rows": [
                    {
                        "columns": [
                            {"widgets": ["param1"]},
                            {"widgets": ["param2"]}
                        ]
                    },
                    {
                        "columns": [
                            {"widgets": ["param3"]},
                            {"widgets": ["param4"]}
                        ]
                    }
                ]
            }
        ]
    }
    
    result = process_layout(wsos, layout_config)
    print(f"Result: {result}")
    
    # Verify grid structure
    assert "containers" in result
    assert len(result["containers"]) == 1
    assert result["containers"][0]["type"] == "grid"
    assert len(result["containers"][0]["rows"]) == 2
    assert len(result["containers"][0]["rows"][0]["columns"]) == 2
    
    print("✓ Grid layout test passed!")
    print()

def test_nested_layouts():
    """Test nested layouts"""
    print("=== Testing Nested Layouts ===")
    
    wsos = [
        {"id": "param1", "type": "text", "label": "Param 1"},
        {"id": "param2", "type": "number", "label": "Param 2"},
        {"id": "param3", "type": "boolean", "label": "Param 3"}
    ]
    
    layout_config = {
        "containers": [
            {
                "type": "section",
                "name": "Main Section",
                "content": [
                    {
                        "type": "tabs",
                        "tabs": [
                            {"name": "Tab 1", "widgets": ["param1"]},
                            {
                                "name": "Tab 2",
                                "content": [
                                    {
                                        "type": "accordion",
                                        "items": [
                                            {"name": "Accordion Item", "widgets": ["param2"]}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    result = process_layout(wsos, layout_config)
    print(f"Result: {result}")
    
    # Verify nested structure
    assert "containers" in result
    assert len(result["containers"]) == 1
    assert result["containers"][0]["type"] == "section"
    assert len(result["containers"][0]["content"]) == 1
    assert result["containers"][0]["content"][0]["type"] == "tabs"
    
    print("✓ Nested layouts test passed!")
    print()

def test_inheritance_backward_compatibility():
    """Test inheritance backward compatibility"""
    print("=== Testing Inheritance Backward Compatibility ===")
    
    wsos = [
        {"id": "param1", "type": "text", "label": "Param 1"},
        {"id": "param2", "type": "number", "label": "Param 2"}
    ]
    
    # Old style layout with sections
    layout_config = {
        "sections": [
            {"name": "Old Style", "widgets": ["param1"]}
        ]
    }
    
    result = process_layout(wsos, layout_config)
    
    # Verify that both sections and containers keys exist
    assert "sections" in result, "sections key should exist for backward compatibility"
    assert "containers" in result, "containers key should exist for new layout system"
    assert len(result["sections"]) == 1, "Should have 1 section"
    assert len(result["containers"]) == 1, "Should have 1 container"
    
    print("✓ Inheritance backward compatibility test passed!")
    print()

if __name__ == "__main__":
    print("Running PyGUIzer Layout Enhancement Tests...")
    print("=" * 50)
    print()
    
    try:
        test_basic_section_layout()
        test_tabs_layout()
        test_accordion_layout()
        test_grid_layout()
        test_nested_layouts()
        test_inheritance_backward_compatibility()
        
        print("=" * 50)
        print("🎉 All layout enhancement tests passed!")
        print("✅ Enhanced layout system is working correctly!")
        print("✅ Backward compatibility is maintained!")
        print("✅ New layout types (tabs, accordion, grid) are supported!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
